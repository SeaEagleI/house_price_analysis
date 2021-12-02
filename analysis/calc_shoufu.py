import numpy as np

from preprocess.json2csv import flatten_dict
import pandas as pd
import copy

data = [
    {
        "totalPrice": 9400000,
        "taxTotal": 602449.97,
        "taxTotalDesc": "60.2",
        "taxFees": [
            {"tax_rule_id": 2156,
             "name": "增值税",
             "expression": "5% * ((成交价-作为增值税原值金额)/1.05)",
             "value": 128571.42
             },
            {
                "tax_rule_id": 2098,
                "name": "增值税附加",
                "expression": "0.3% * ((成交价-作为增值税原值金额)/1.05)",
                "value": 7714.28
            },
            {"tax_rule_id": 2057,
             "name": "契税",
             "expression": "(成交价-增值税) * 1.5%",
             "value": 132021.42
             },
            {
                "tax_rule_id": 2122,
                "name": "个人所得税",
                "expression": "(成交价-增值税-作为个人所得税原值金额-原契税实缴金额-增值税附加-成交价*0.1-银行利息) * 20%",
                "value": 334142.85
            }
        ],
    },
]
# csv_data = []
# for sample in data:
#     line = {}
#     for i in flatten_dict(sample):
#         line[".".join(i[:-1])] = i[-1]
#     csv_data.append(copy.deepcopy(line))
# df = pd.DataFrame(csv_data)
# print(df)
# df.to_clipboard(sep="\t")

# 背景知识
# 贷款还款方式: 1）等额本息: 每月等额还款; 2）等额本金: 递减还款, 存在每月递减, 包含一定超前还款成分
# 贷款类型: 商业贷款、公积金贷款、二者组合
# 银行计算贷款的依据是评估价，而评估价一般是成交价的90%~95%
# 北京市的现行政策：
# 1）在首套房的情况下，首付最低比例为35%评估价（实际交易使用成交价，故实际首付比例远不止35%），
#    即所有类型贷款的本金总和不超过评估价的65%（如组合贷款中【商业贷款本金】和【公积金本金】之和）
# 2）商业贷款利率4.9%，公积金贷款利率3.25%，首套房的公积金贷款最高140w，单人的公积金每套房最多贷款70w
# 现实标准：
# 1）买卖双方交易的税（增值税、契税、个税）均由买方承担, 表现在首付里, 故: 实际最低首付 = 成交价 - 65%×评估价 + 税费合计
# 2) 税费中的增值税、个税严重受卖方该房是否“满五”、是否“唯一”、以及上次成交价格（原值）影响，波动很大

# 假设
# 1. 家庭的年支出稳定，每年用30w来还款，即: return_year = 30 (每年无超出outcome_year的还款、及还款外开支)
# 2. 还款期限为30年，期间每月末还款一次, 不提前还款, 采用<等额本息>方式还款 (便于计算)
# 3. 贷款方式: 组合贷款 (公积金贷款金额 + 商贷金额 = 成交价 * 65%)
# 4. 买方为首套房 => 贷款比例上界65%，公积金贷款最高140w（且该家庭恰好有2人30年内均拿稳定的公积金，每人可支持70w公积金贷款）
# 5. 银行采用的评估价按成本价的95%计，即: evaluation = total_price * 0.95
# basic info
years = 30
turns = years * 12
eval_price_ratio = 0.95
person = 2
# return
return_year = 30
# loan
loan_prop = 0.65  # 首套房组合贷款比例上界
acc_fund_interest = 0.0325
business_interest = 0.049
acc_fund_loan = min(70 * person, 140)
# total_price = 730
# evaluation = int(total_price * eval_price_ratio)
# business_loan = evaluation * loan_prop - acc_fund_loan
# calc monthly return
# business_debx = calc_debx(business_loan, years, business_interest)
# acc_fund_debx = calc_debx(acc_fund_loan, years, acc_fund_interest)
# total_debx = business_debx + acc_fund_debx
# tax: an extra part of shoufu above pure_shoufu (SKIP)
# 	0	1
# 总价	9400000	7250000
# 原值	6700000.18	1160000
# 税费合计	602449.97	1425170
# 税费合计（万元）	60.2	142.5
# 1.增值税	(成交价-作为增值税原值金额)/21
# 	128571.42	290000
# 2.增值税附加	(成交价-作为增值税原值金额)/350
# 	7714.2852	17400
# 	7714.28	17400
# 3.契税	(成交价-增值税) * 0.015
# 	134323.8574	97196.4
# 	132021.42	98850
# 4.个人所得税	(成交价-增值税-作为个人所得税原值金额-原契税实缴金额-增值税附加-成交价*0.1-银行利息) * 0.2
# 	334142.85	1018920
# shoufu
# pure_shoufu = total_price - business_loan - acc_fund_loan


# 等额本金（每月递减）
def calc_debj(loan, y, i):
    loan *= 1e4
    return np.array([(y * i + 1) * loan / (12 * y), loan * i / (144 * y)])


# 等额本息（等额还款）
def calc_debx(loan, y, i):
    loan *= 1e4
    mi = i / 12
    p = pow(1 + mi, 12 * y)
    return mi * loan * p / (p - 1)


# 等额本息反向计算（由月供算贷款本金）
def rev_debx(loan_month, y, i):
    mi = i / 12
    p = pow(1 + mi, 12 * y)
    return loan_month / mi / p * (p-1) / 1e4


# 由年还款算最大贷款
def get_max_loan(return_year):
    return_month = return_year * 1e4 / 12
    acc_fund_debx = calc_debx(acc_fund_loan, years, acc_fund_interest)
    max_business_debx = return_month - acc_fund_debx
    max_business_loan = rev_debx(max_business_debx, years, business_interest)
    return max_business_loan + acc_fund_loan


if __name__ == "__main__":
    print(get_max_loan(30))
    print(get_max_loan(20))
    print(get_max_loan(10))

