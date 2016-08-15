# -*- coding: utf-8 -*-

from openerp import models, fields, api

class BloodClinic(models.Model):
    _name = "mqc.blood.clinic"
    _description = u'全院临床用血情况'

    report_month = fields.Char( u'上报月份', )
    units_name = fields.Char( u'单位名称',)
    units_code = fields.Char(u'单位编码', )

    out_case = fields.Integer( u'出院总人数', )
    use_blood_case = fields.Integer(u'用血总人数',)
    opr_num  = fields.Integer(u'手术台数',)
    opr_use_blood = fields.Integer( u'手术用血人数',)
    whole_blood = fields.Integer( u'全血',)
    short_sign1 = fields.Char(u'全血是否短缺',)
    rbc = fields.Integer(u'红细胞',)
    short_sign2 = fields.Char(u'红细胞是否短缺',)
    plasma = fields.Integer(u'血浆',)
    short_sign3 = fields.Char(u'血浆是否短缺',)
    platelet = fields.Integer( u'血小板',)
    short_sign4 = fields.Char(u'血小板是否短缺',)
    cryoprecipitate = fields.Integer( u'冷沉淀',)
    short_sign5 = fields.Char(u'冷沉淀是否短缺',)

    total_usage = fields.Integer(u'本月用血量合计',)
    self_storage = fields.Integer( u'储存式',)
    self_storage_case = fields.Integer(u'储存式人数',)
    self_recycle = fields.Float(u'回收式',)
    self_recycle_case = fields.Integer(  u'回收式人数',)
    dilution = fields.Integer(u'稀释式',)
    dilution_case = fields.Integer(u'稀释式人数',)
    total_self_usage = fields.Integer( u'自体输血量',)
    total_self_case = fields.Integer( u'自体输血数',)
    component_rate = fields.Integer(  u'成分输血率',)
    self_rate = fields.Integer( u'自体输血率',)
    avg_usage= fields.Integer(u'住（出）院患者人均用血量',)

class Blood(models.Model):
    _name = "mqc.blood"
    _description = u"输血填报"
    _inherits = {'mqc.mqc': 'mqc_id'}
    # _inherit = 'mqc.mqc'
    mqc_id = fields.Many2one('mqc.mqc', u'报表id', required=True,
                              ondelete='cascade')
    report_clinic = fields.Many2one('mqc.blood.clinic', u'全院临床用血情况')
    report_construct = fields.Many2one('mqc.blood.construct', u'输血科建设及检测技术')
    report_qlty = fields.Many2one('mqc.blood.qlty', u'血液成分质量反馈')
    report_manager = fields.Many2one('mqc.blood.manage', u'输血职能管理')
    report_advise = fields.Many2one('mqc.blood.advise', u'质量安全工作意见')


#相关字典
class BloodTech(models.Model):
    _name = "mqc.blood.tech"
    _description = u"输血科检测技术"
    name = fields.Char(u'技术名称',)

class BloodComp(models.Model):
    _name = "mqc.blood.component"
    _description = u"血液成分"
    name = fields.Char(u'成分名称',)

class BloodManageItem(models.Model):
    _name = "mqc.blood.quota"
    _description = u"输血管理指标"
    name = fields.Char(u'指标名称',)

class BloodReact(models.Model):
    _name = "mqc.blood.react"
    _description = u"不良反应"
    name = fields.Char(u'名称',)


class BloodConstructDetail(models.Model):
    _name = "mqc.blood.construct.detail"
    _description = u"输血科建设及检测技术明细"

    tech_id = fields.Many2one('mqc.blood.tech',u'输血科检测技术',required=True, )
    construct_id = fields.Many2one('mqc.blood.construct',u'主记录',required=True, )
    #关联技术字典
    tech_name = fields.Char(u'技术名称', related='tech_id.name', readonly=False, store=True, )
    opr_method = fields.Char( u'操作方法',required=True,)

    cases = fields.Integer(u'例数', )
    indoor_qc_freq = fields.Integer(u'室内质控频率', )
    province_eqa = fields.Char(u'省室间质评结果', ) # eqa  = external quality assessment
    country_eqa = fields.Char(u'国室间质评结果', )

class BloodConstruct(models.Model):
    _name = "mqc.blood.construct"
    _description = u'输血科建设及检测技术'

    report_month = fields.Char( u'上报月份',)
    units_name = fields.Char( u'单位名称',)
    units_code = fields.Char(u'单位编码',)
    create_type = fields.Selection([('01', u'独立建制'), ('02', u'未设独立建制')],
                                   u'输血科或血库建制')
    dept_emp_num = fields.Integer(u'科室人数',)
    bed_num = fields.Integer( u'医院床位数',)
    required_device  = fields.Selection([('01', u'齐全'), ('02', u'不齐全')], u'科室必需设备')
    shortage_device = fields.Char(u'缺少的设备名称',)
    detail_ids = fields.One2many('mqc.blood.construct.detail', 'construct_id', u'技术明细')

#表3 血液成分质量反馈月报表
class BloodQuality(models.Model):
    _name = "mqc.blood.qlty"
    _description = u'血液成分质量'

    report_month = fields.Char( u'上报月份',)
    units_name = fields.Char( u'单位名称',)
    units_code = fields.Char(u'单位编码',)
    detail_ids = fields.One2many('mqc.blood.qlty.detail', 'qlty_id', u'质量明细') #关联明细

class BloodQualityDetail(models.Model):
    _name = "mqc.blood.qlty.detail"
    _description = u"血液成分质量明细"

    component_id = fields.Many2one('mqc.blood.component',u'血液成分',required=True, )
    qlty_id = fields.Many2one('mqc.blood.qlty',u'主记录',required=True, ) #关联主记录
    qlty_des = fields.Char(u'质量问题描述',)
    bld_bag_no = fields.Char( u'血袋编码',)
    bld_spec = fields.Integer(u'血液规格', )

#表4 输血职能管理月报表
class BloodManage(models.Model):
    _name = "mqc.blood.manage"
    _description = u'输血职能管理'

    report_month = fields.Char( u'上报月份',)
    units_name = fields.Char( u'单位名称',)
    units_code = fields.Char(u'单位编码',)
    detail_ids = fields.One2many('mqc.blood.manage.detail', 'manage_id', u'项目明细') #关联明细
    react_ids = fields.One2many('mqc.blood.manage.react', 'manage_id', u'不良反应报告') #关联明细

class BloodManageReact(models.Model):
    _name = "mqc.blood.manage.react"
    _description = u"输血管理不良报告"
    react_id = fields.Many2one('mqc.blood.react',u'不良反应',required=True, )
    manage_id = fields.Many2one('mqc.blood.manage', u'主记录', required=True, )  # 关联主记录
    cases = fields.Char( u'例数',)


class BloodManageDetail(models.Model):
    _name = "mqc.blood.manage.detail"
    _description = u"输血管理项目明细"
    quota_id = fields.Many2one('mqc.blood.quota',u'管理项目名称',required=True, )
    manage_id = fields.Many2one('mqc.blood.manage',u'主记录',required=True, ) #关联主记录
    rate = fields.Char(u'百分率',)
    remark = fields.Char( u'备注',)

#表5 临床用血质量安全工作意见反馈
class BloodAdvise(models.Model):
    _name = "mqc.blood.advise"
    _description = u'质量安全工作意见反馈'

    report_month = fields.Char( u'上报月份',)
    units_name = fields.Char( u'单位名称',)
    units_code = fields.Char(u'单位编码',)
    advise = fields.Text(u'您对临床用血质量安全与质控工作的建议',)
    safe_advise = fields.Text(u'您认为目前输血工作中尚存在的安全隐患',)

