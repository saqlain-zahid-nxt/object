# Copyright (c) 2025, nextash and contributors
# For license information, please see license.txt

# Copyright (c) 2025, NexTash (SMC-PVT) Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions

def execute(filters=None):
    if not filters:
        filters = {}

    currency = frappe.get_cached_value("Company", filters.get("company"), "default_currency") if filters.get("company") else frappe.defaults.get_global_default("currency")
    columns = get_columns(filters, currency)
    data = get_data(filters)

    return columns, data


def get_columns(filters, currency):
    columns = [
        {
            "label": _("GL Entry"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "GL Entry",
            "hidden": 1,
        },
        {"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 100},
        {
            "label": _("Account"),
            "fieldname": "account",
            "fieldtype": "Link",
            "options": "Account",
            "width": 180,
        },
        {
            "label": _("Debit ({0})").format(currency),
            "fieldname": "debit",
            "fieldtype": "Float",
            "width": 130,
        },
        {
            "label": _("Credit ({0})").format(currency),
            "fieldname": "credit",
            "fieldtype": "Float",
            "width": 130,
        },
        {
            "label": _("Balance ({0})").format(currency),
            "fieldname": "balance",
            "fieldtype": "Float",
            "width": 130,
        },
        {"label": _("Voucher Type"), "fieldname": "voucher_type", "width": 120},
        {
            "label": _("Voucher Subtype"),
            "fieldname": "voucher_subtype",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 180,
        },
        {"label": _("Against Account"), "fieldname": "against", "width": 120},
        {"label": _("Party Type"), "fieldname": "party_type", "width": 100},
        {"label": _("Party"), "fieldname": "party", "width": 100},
    ]

    columns.append({"label": _("Project"), "options": "Project", "fieldname": "project", "width": 100})

    columns.append(
        {"label": _("Cost Center"), "options": "Cost Center", "fieldname": "cost_center", "width": 100}
    )

    columns.extend(
        [
            {"label": _("Against Voucher Type"), "fieldname": "against_voucher_type", "width": 100},
            {
                "label": _("Against Voucher"),
                "fieldname": "against_voucher",
                "fieldtype": "Dynamic Link",
                "options": "against_voucher_type",
                "width": 100,
            },
        ]
    )

    columns.append({"label": _("Remarks"), "fieldname": "remarks", "width": 400})

    return columns


def get_data(filters):
    if not (filters.get("from_date") and filters.get("to_date") and filters.get("project")):
        return []

    sql_filters = {
        "from_date": filters.get("from_date"),
        "to_date": filters.get("to_date"),
        "project": filters.get("project")
    }

    dimension_fields = ""

    if filters.get("include_dimensions"):
        for dim in get_accounting_dimensions(as_list=False):
            dimension_fields += f", gle.`{dim.fieldname}`"
        dimension_fields += ", gle.cost_center"

    query = f"""
        SELECT
            gle.name,
            gle.posting_date,
            gle.account,
            gle.debit,
            gle.credit,
            gle.voucher_type,
            gle.voucher_subtype,
            gle.voucher_no,
            gle.against,
            gle.party_type,
            gle.party,
            gle.project
            {dimension_fields},
            gle.against_voucher_type,
            gle.against_voucher,
            gle.remarks
        FROM `tabGL Entry` gle
        INNER JOIN `tabAccount` acc ON gle.account = acc.name
        WHERE
            gle.docstatus = 1
            AND gle.is_cancelled = 0
            AND gle.voucher_type != "Payment Entry"
            AND gle.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND gle.project = %(project)s
            AND IFNULL(acc.parent_account, '') != 'Direct Income - Operation'
            AND IFNULL(acc.account_type, '') != 'Round Off'
        ORDER BY gle.posting_date ASC
    """

    data = frappe.db.sql(query, sql_filters, as_dict=1)

    balance = 0
    for row in data:
        balance += flt(row.get("debit", 0)) - flt(row.get("credit", 0))
        row["balance"] = balance

    total_debit = sum(flt(row.get("debit", 0)) for row in data)
    total_credit = sum(flt(row.get("credit", 0)) for row in data)
    profit = total_debit - total_credit

    data.append({
        "account": _("Total Income"),
        "debit": total_debit,
    })

    data.append({
        "account": _("Total Expense"),
        "credit": total_credit,
    })

    data.append({
        "account": _("Profit/Loss"),
        "balance": profit
    })

    return data