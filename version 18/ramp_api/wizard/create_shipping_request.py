from odoo import api, fields, models, _
from odoo import http
import pprint
import requests
import json


# The below is the wizard view
class CreateShipping(models.TransientModel):
    _name = "create.shipping.request.wizard"
    _description = "Create Shipping Request"

    picking_id = fields.Many2one('stock.picking', string="Picking Reference")
    name = fields.Char(string="Name")
    address = fields.Char(string="Address")
    consignee_state = fields.Char(string="State")
    consignee_city = fields.Char(string="City")
    consignee_phone = fields.Char(string="Phone")
    cargo_value = fields.Float(string="Cargo Value")
    cod = fields.Float(string="COD", related="cargo_value")
    description = fields.Text(string="Description")
    sales_order_seq = fields.Char(string="ReferenceNumber")

    # Step Four: calling (default_get) method: to when open wizard variables filling automatically
    @api.model
    def default_get(self, fields_list):
        res = super(CreateShipping, self).default_get(fields_list)

        if self.env.context.get('default_picking_id'):
            res['picking_id'] = self.env.context.get('default_picking_id')
        if self.env.context.get('default_address'):
            res['address'] = self.env.context.get('default_address')
        if self.env.context.get('default_name'):
            res['name'] = self.env.context.get('default_name')
        if self.env.context.get('default_phone'):
            res['consignee_phone'] = self.env.context.get('default_phone')
        if self.env.context.get('default_state'):
            res['consignee_state'] = self.env.context.get('default_state')
        if self.env.context.get('default_city'):
            res['consignee_city'] = self.env.context.get('default_city')
        if self.env.context.get('default_sale_total'):
            res['cargo_value'] = self.env.context.get('default_sale_total')
        if self.env.context.get('default_description'):
            res['description'] = self.env.context.get('default_description')
        if self.env.context.get('default_sale_name'):
            res['sales_order_seq'] = self.env.context.get('default_sale_name')

        return res


    # Step five: make button at the wizard send request to API
    def create_shipping(self):
        """This method is called from the wizard button"""
        for rec in self:

            # State mapping dictionary - Odoo name: RAMP API name
            state_mapping = {
                'Asyut': 'Assuit',
                'Beni Suef': 'Baniswif',
                'Faiyum': 'Fayoum',
                'South Sinai': 'Southsinai',
                'Qalyubia': 'Qalyoubia',
                'Kafr el-Sheikh': 'Kafrelsheikh',
                'Port Said': 'Portsaid',
                'Sohag': 'Souhag',
                'Al Sharqia': 'Sharkia',
                # Add more mappings as needed
            }

            # Get the mapped state name
            ramp_state = state_mapping.get(rec.consignee_state, rec.consignee_state)
            # Works like this:
            # 1. Look for key 'Asyut' in dictionary ✓ (found)
            # 2. Get the value for 'Asyut' → 'Assuit'
            # 3. Assign 'Assuit' to ramp_state

            # Result: ramp_state = 'Assuit'

            waybill_data = {
                "waybillRequestData": {
                    "FromOU": "WAHAHUB",
                    "WaybillNumber": "",
                    "DeliveryDate": "",
                    "ClientCode": "TEST",

                    "CustomerCode": "TEST",
                    "ConsigneeCode": "00000",

                    "ConsigneeAddress": rec.address,
                    "ConsigneeCountry": "EG",
                    "ConsigneeState": ramp_state,
                    "ConsigneeCity": rec.consignee_city,
                    "ConsigneeName": rec.name,
                    "ConsigneePhone": rec.consignee_phone,
                    "NumberOfPackages": "1",
                    "ActualWeight": "1.0",
                    "ChargedWeight": "1.0",
                    "CargoValue": str(rec.cargo_value),
                    "PaymentMode": "TBB",
                    "ServiceCode": "PUD",
                    "WeightUnitType": "KILOGRAM",
                    "Description": rec.description,
                    "ReferenceNumber": rec.sales_order_seq,
                    "COD": str(rec.cod),
                    "CODPaymentMode": "Cash",
                    "CreateWaybillWithoutStock": "false"
                }
            }

            # Pretty print the request data
            print("=== WAYBILL REQUEST DATA ===")
            print(f"ConsigneeState value: {rec.consignee_state}")
            print(json.dumps(waybill_data, indent=4))
            # json.dumps() => This converts a Python dictionary/object into a formatted JSON string:
            # indent=4 => To view the formatted JSON string like dictionary(waybill_data), Not print in one line

            try:
                url = "https://webservice.logixerp.com/webservice/v2/CreateWaybill?secureKey=A049E85FB20843CEA981CA6A281E7DA8"

                headers = {
                    'Content-Type': 'application/json',
                }
                # Headers tell the server what type of data you're sending:
                # Content-Type: application/json => tells the API server "I'm sending JSON data, not form data or plain text"

                response = requests.post(url, json=waybill_data, headers=headers, timeout=30)
                # This sends an HTTP POST request to the API:
                # requests.post() => makes a POST request (sending data TO the server)
                # json=waybill_data => automatically converts your dictionary to JSON and sends it

                print("=== API RESPONSE ===")
                print(f"Response: {response}") # => <Response [200]>
                print(f"Status Code: {response.status_code}")

                if response.status_code == 200:
                    response_data = response.json()
                    # Save the response data to the database
                    print("SUCCESS!")
                    print("Response JSON:")
                    # print(response.json()) # => {'labelURL': 'https://s3.amazonaws.com/rachna-prod/A049E85FB20843CEA981CA6A281E7DA8/Docket/RAMPLOGISTICS_INTERNAL_2025_10120/RM00026242.pdf', 'message': 'WayBill Created Successfully', 'messageType': 'Success', 'packageStickerURL': 'https://s3.amazonaws.com/rachna-prod/A049E85FB20843CEA981CA6A281E7DA8/Temp/RM00026242.pdf', 'status': 'Data Received', 'trackingURL': 'http://webservice.logixerp.com/webservice/v2/ShipmentTracking?w=mPW/ahvEjn87L5wehervaUtk+R0A2JAAmv8kgL1P/CIZs3jxFNfGLmoSEFx5zJv5', 'waybillNumber': 'RM00026242'}
                    print(json.dumps(response.json(), indent=4))
                    # json.dumps() => converts it back to a formatted JSON string to use (indent=4) to make print like output of postman

                    # Send the response data to smart button form
                    self.env['ramp.api.response'].create({
                        'picking_id': rec.picking_id.id,
                        'sale_number': self.sales_order_seq,
                        'labelURL': response_data.get('labelURL', ''),
                        'message': response_data.get('message', ''),
                        'messageType': response_data.get('messageType', ''),
                        'packageStickerURL': response_data.get('packageStickerURL', ''),
                        'status': response_data.get('status', ''),
                        'trackingURL': response_data.get('trackingURL', ''),
                        'waybillNumber': response_data.get('waybillNumber', ''),
                    })

                else:
                    print("ERROR!")
                    print(f"Response Text: {response.text}")

            except Exception as e:
                print("=== CONNECTION ERROR ===")
                print(f"Error: {str(e)}")

