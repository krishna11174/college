from odoo import api, fields, models, SUPERUSER_ID, _
import json
import requests

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def get_url(self):
        return self.env['res.config.settings'].search([],order='id desc',limit=1).cf_api_url

    def get_key(self):
        return self.env['res.config.settings'].search([],order='id desc',limit=1).cf_api_key

    cf_api_url = fields.Char("Server URL",default=get_url)
    cf_api_key = fields.Char("API Key",default=get_key)

class AggregatedInventory(models.Model):
    _name = 'aggregated.inventory'

    warehouse_ref = fields.Char()
    product_ref = fields.Char()
    quantity = fields.Float()

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    warehouse_ref = fields.Char(compute='get_codes',store=True)
    product_ref = fields.Char(compute='get_codes',store=True)
    aggregate_qty = fields.Float(compute='compute_aggregate',store=True)

    @api.depends('location_id','product_id')
    def get_codes(self):
        for rec in self:
            if rec.location_id.is_bin:
                rec.warehouse_ref = self.env['stock.location'].search([('id','=',int(rec.location_id.parent_path.split('/')[1]))]).name
            else:
                rec.warehouse_ref = False
            if rec.product_id.default_code:
                rec.product_ref = rec.product_id.default_code
            else:
                rec.product_ref = False

    @api.depends('warehouse_ref','product_ref','quantity')
    def compute_aggregate(self):
        
        API_ENDPOINT = self.env['res.config.settings'].search([],order='id desc',limit=1).cf_api_url

        headers = {
            "Content-Type":"application/json",
            "x-api-key":self.env['res.config.settings'].search([],order='id desc',limit=1).cf_api_key
        }

        prod_quant_list = []

        for rec in self:
            if rec.warehouse_ref and rec.product_ref:
                
                quants = self.env['stock.quant'].search([
                    ('warehouse_ref','=',rec.warehouse_ref),
                    ('product_ref','=',rec.product_ref)])
                
                quantity = 0
                
                for quant in quants:
                    quantity += quant.quantity
                
                aggregate = self.env['aggregated.inventory'].search([
                    ('warehouse_ref','=',rec.warehouse_ref),
                    ('product_ref','=',rec.product_ref)])

                if aggregate.quantity != quantity:
                    aggregate.write({'quantity':quantity})

                else:
                    aggregate = self.env['aggregated.inventory'].create({
                        'warehouse_ref':rec.warehouse_ref,
                        'product_ref':rec.product_ref,
                        'quantity':quantity})
                
                rec.aggregate_qty = quantity

                prod_quant_list.append({
                    'product_ref': aggregate.product_ref,
                    'location_ref': aggregate.warehouse_ref,
                    'quantity': quantity
                    })

            else:
                rec.aggregate_qty = 0

        payload = {
            "inventoryUpdateRequest":prod_quant_list
        }

        response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(payload))
        print(response)

    def liquid_cure(self,warehouse_ref,product_ref_qty,transaction_ref):
        print(warehouse_ref)
        print(product_ref_qty)

        warehouse = self.env['stock.warehouse'].search([('code','=',warehouse_ref)])
        print('warehouse : ',warehouse.id)

        operation = self.env['stock.picking.type'].search([
            ('code','=','outgoing'),
            ('warehouse_id','=',warehouse.id)])
        print('operation : ',operation.barcode)


        move = []
        for product in product_ref_qty.keys():
            pid = self.env['product.product'].search([('default_code','=',product)])
            move.append((0,0,{
                'name' : '%s: [%s]%s'%(transaction_ref,product,pid.name),
                'product_id' : pid.id,
                'product_uom_qty' : product_ref_qty[product],
                'product_uom' : pid.uom_id.id}))

        picking = self.env['stock.picking'].create({
            'origin' : transaction_ref,
            'picking_type_id' : operation.id,
            'location_id' : operation.default_location_src_id.id,
            'location_dest_id' : 5,
            'move_ids_without_package' : move
            })
        print('picking : ',picking.id)


        picking.action_confirm()
        picking.action_assign()

        for line in picking.move_line_ids_without_package:
            line.qty_done = line.product_uom_qty

        picking.button_validate()


        return (warehouse_ref,product_ref_qty)
