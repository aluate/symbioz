"""
Tax-related enums
"""

import enum


class FilingStatusEnum(str, enum.Enum):
    SINGLE = "single"
    MARRIED_FILING_JOINT = "married_filing_joint"
    MARRIED_FILING_SEPARATE = "married_filing_separate"
    HOH = "head_of_household"


class TaxBucketEnum(str, enum.Enum):
    NONE = "none"
    W2_WAGES = "w2_wages"
    BUSINESS_INCOME = "business_income"
    BUSINESS_EXPENSE = "business_expense"
    MORTGAGE_INTEREST = "mortgage_interest"
    PROPERTY_TAX = "property_tax"
    CHARITABLE = "charitable"
    MEDICAL = "medical"
    EDUCATION = "education"
    RETIREMENT = "retirement"
    HSA = "hsa"
    CHILDCARE = "childcare"
    INVESTMENT_INCOME = "investment_income"
    OTHER_INCOME = "other_income"


class TaxDocumentTypeEnum(str, enum.Enum):
    W2 = "w2"
    FORM_1099_MISC = "1099_misc"
    FORM_1099_NEC = "1099_nec"
    FORM_1099_INT = "1099_int"
    FORM_1099_DIV = "1099_div"
    FORM_1098 = "1098"           # mortgage interest
    FORM_1098_T = "1098_t"       # tuition
    FORM_1098_E = "1098_e"       # student loan interest
    STATEMENT = "statement"      # general statement

