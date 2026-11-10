/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { OrderSummary } from "@point_of_sale/app/screens/product_screen/order_summary/order_summary";

const originalDiscountByLine = new WeakMap();
const activeDiscountEditByLine = new WeakMap();

function rememberOriginalDiscount(line) {
    if (line) {
        originalDiscountByLine.set(line, line.get_discount());
    }
}

patch(ProductScreen.prototype, {
    onNumpadClick(buttonValue) {
        if (buttonValue === "discount") {
            rememberOriginalDiscount(this.currentOrder?.get_selected_orderline());
        }
        return super.onNumpadClick(...arguments);
    },
});

patch(OrderSummary.prototype, {
    clickLine(ev, orderline) {
        rememberOriginalDiscount(orderline);
        return super.clickLine(...arguments);
    },

    _setValue(val) {
        const line = this.currentOrder.get_selected_orderline();
        if (this.pos.numpadMode !== "discount" || val === "remove" || !line) {
            return super._setValue(...arguments);
        }

        if (!originalDiscountByLine.has(line)) {
            rememberOriginalDiscount(line);
        }
        activeDiscountEditByLine.set(line, originalDiscountByLine.get(line));
        try {
            return super._setValue(...arguments);
        } finally {
            activeDiscountEditByLine.delete(line);
        }
    },
});

patch(PosStore.prototype, {
    async setDiscountFromUI(line, val) {
        const discount = typeof val === "number" ? val : parseFloat(val);
        if (discount > 10) {
            if (activeDiscountEditByLine.has(line)) {
                line.set_discount(activeDiscountEditByLine.get(line));
            }
            this.dialog.add(AlertDialog, {
                title: _t("Invalid discount"),
                body: _t("You cannot add more than 10% discount."),
            });
            return;
        }
        return super.setDiscountFromUI(...arguments);
    },
});
