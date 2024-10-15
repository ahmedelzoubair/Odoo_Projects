from odoo import models, fields

class ModelRelationsExporter(models.TransientModel):
    _name = 'model.relations.exporter'
    _description = 'Export Model Relations'

    name = fields.Char(string='Export Name', readonly=True, default='Model Relations Viewer')
    relations_output = fields.Text(string='Model Relations', readonly=True)

    def export_relations(self):
        models_relations = []
        for model_name in self.env:
            model = self.env[model_name]
            if model._abstract:
                continue  # Skip abstract models
            fields = model.fields_get()
            for field_name, field_info in fields.items():
                relation = field_info.get('relation')
                ttype = field_info.get('type')
                if relation:
                    models_relations.append(
                        f"Model: {model_name} | Field: {field_name} | Type: {ttype} | Related Model: {relation}"
                    )

        # Join the relations into a single text string
        relations_output = "\n".join(models_relations)

        # Display the relations in the field
        self.write({
            'relations_output': relations_output
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'target': 'new',
        }
