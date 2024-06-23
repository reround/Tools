from ..basic.basic import *

import numpy as np


class Beam_splitter:
    def __init__(self, ratio=(1, 1)):
        """分束器

        Args:
            ratio (tuple, optional): 分束比例. Defaults to (1, 1).
        """
        self.ratio = ratio

    def output_power(self, p_i):
        """Calculate the out power of beam splitter

        Args:
            p_i (_type_): Input power

        Returns:
            _type_: output power 1, putput power 2
        """
        p_o1 = p_i * (self.ratio[0] / (self.ratio[0] + self.ratio[1]))
        p_o2 = p_i - p_o1
        return p_o1, p_o2


class flange:
    def __init__(self, loss=-0.1):
        """法兰

        Args:
            loss (float, optional): Loss of flange. Defaults to -0.1.
        """
        self.loss = loss

    def output_power(self, p_i):
        """Calculate the out power of flange

        Args:
            p_i (_type_): Input power
            loss (_type_): Loss of flange (dB)

        Returns:
            _type_: output power
        """
        return loss(p_i, self.loss)


class coupler_2x2:
    def __init__(
        self,
        ratio=(50, 50),
        IL_11=-3.49,
        IL_12=-3.36,
        IL_21=-3.23,
        IL_22=-3.28,
        PDL_11=-0.03,
        PDL_12=-0.03,
        PDL_21=-0.03,
        PDL_22=-0.05,
        loss_r=-55,
    ):
        """2x2 耦合器

        Args:
            ratio (tuple, optional): Ratio. Defaults to (50, 50).
        IL_11 (float, optional): Insertion loss from first in port to first out port. Defaults to -3.49.
        IL_12 (float, optional): Insertion loss from first in port to second out port. Defaults to -3.36.
        IL_21 (float, optional): Insertion loss from second in port to first out port. Defaults to -3.23.
        IL_22 (float, optional): Insertion loss from second in port to second out port. Defaults to -3.28.
        PDL_11 (float, optional): Polarization Dependent Loss from first in port to first out port. Defaults to -0.03.
        PDL_12 (float, optional): Polarization Dependent Loss from first in port to second out port. Defaults to -0.03.
        PDL_21 (float, optional): Polarization Dependent Loss from second in port to first out port. Defaults to -0.03.
        PDL_22 (float, optional): Polarization Dependent Loss from second in port to second out port. Defaults to -0.05.
        loss_r (int, optional): Loss of return. Defaults to 55.
        """
        self.ratio = ratio
        self.IL_11 = IL_11
        self.IL_12 = IL_12
        self.IL_21 = IL_21
        self.IL_22 = IL_22
        self.PDL_11 = PDL_11
        self.PDL_12 = PDL_12
        self.PDL_21 = PDL_21
        self.PDL_22 = PDL_22
        self.loss_r = loss_r

    # FIXME:没有计算混频功率
    def output_power(
        self,
        p_1_i,
        p_2_i,
    ):
        """Calculate output power of 2 x 2 coupler

        Args:
            p_1_i (_type_): Input power of first input port
            p_2_i (_type_): Input power of second input port
        """
        # r = self.ratio[0] / (self.ratio[0] + self.ratio[1])
        # p_1_i_to_1 = p_1_i * r
        # p_1_i_to_2 = p_1_i - p_1_i_to_1

        # p_2_i_to_1 = p_2_i * r
        # p_2_i_to_2 = p_2_i - p_2_i_to_1

        # p_o_1_1 = loss(p_1_i_to_1, self.IL_11)
        # p_o_1_2 = loss(p_1_i_to_2, self.IL_12)
        # p_o_2_1 = loss(p_2_i_to_1, self.IL_21)
        # p_o_2_2 = loss(p_2_i_to_2, self.IL_22)

        # p_o_1 = p_o_1_1 + p_o_2_1
        # p_o_2 = p_o_1_2 + p_o_2_2

        r = self.ratio[0] / (self.ratio[0] + self.ratio[1])
        p_o_1_1 = p_1_i * r
        p_o_1_2 = p_1_i - p_o_1_1
        p_o_2_1 = p_2_i * r
        p_o_2_2 = p_2_i - p_o_2_1
        p_o_1 = p_o_1_1 + p_o_2_1
        p_o_2 = p_o_1_2 + p_o_2_2

        return p_o_1, p_o_2


class circulator:
    def __init__(
        self,
        port="1",
        loss12=-1.1,
        loss23=-1.1,
        loss21=-40,
        loss32=-40,
        loss_typical_excess=-0.25,
    ):
        """环形器

        Args:
            port (str, optional): port. Defaults to "1".
            loss12 (float, optional): Loss from first port to second port. Defaults to -1.1.
            loss23 (float, optional): Loss from second port to third port. Defaults to -1.1.
            loss21 (int, optional): Loss from second port to first port. Defaults to -40.
            loss32 (int, optional): Loss from third port to second port. Defaults to -40.
            loss_typical_excess (float, optional): _description_. Defaults to -0.25.
        """
        self.port = port
        self.loss12 = loss12
        self.loss23 = loss23
        self.loss21 = loss21
        self.loss32 = loss32
        self.loss_typical_excess = loss_typical_excess

    def output_power(self, p_i, port="1"):
        """Calculate the out power of circulator

        Args:
            p_i (_type_): Input power
            port (str, optional): port. Defaults to "1".

        Returns:
            _type_: Out power of the next port.
        """
        if self.port not in ["1", "2"]:
            raise ValueError(
                f"Invalid port value. Expected '1' or '2', but got {self.port}."
            )
        if self.port == "1":
            return loss(p_i, self.loss12)
        if self.port == "2":
            return loss(p_i, self.loss23)


class PDB:
    def __init__(
        self,
        Detector_Material="InGaAs",
        Operating_Wavelength_Range=(800, 1700),
        Max_Responsivity_typ=1.0,
        Detector_Active_Area=0.3e-3,
        RF_OUTPUT_Bandwidth=100e6,
        CMRR=26,
        RF_OUTPUT_Transimpedance_Gains=50e3,
        RF_OUTPUT_Conversion_Gain=50e3,
        CW_Saturation_Power=72e-6,
        Minimum_NEP=6.99e-12,
    ):
        """PDB 平衡探测器

        Args:
            Detector_Material (str, optional): 探测器材料. Defaults to "InGaAs".
            Operating_Wavelength_Range (tuple, optional): 工作波长范围. Defaults to (800, 1700).
            Max_Responsivity_typ (float, optional): 最大响应性，典型值 A/W. Defaults to 1.0.
            Detector_Active_Area (_type_, optional): \phi 探测器有效面积，直径. Defaults to 0.3e-3.
            RF_OUTPUT_Bandwidth (_type_, optional): 射频输出带宽（-3 dB）DC-100 MHz. Defaults to 100e6.
            CMRR (int, optional): 共模抑制比（CMRR）dB. Defaults to 26.
            RF_OUTPUT_Transimpedance_Gains (_type_, optional): 射频输出跨阻增益. Defaults to 50e3 V/A.
            RF_OUTPUT_Conversion_Gain (_type_, optional): 射频输出转换增益. Defaults to 50e3 V/W.
            CW_Saturation_Power (_type_, optional): CW饱和功率. Defaults to 72e-6 W.
            Minimum_NEP (float, optional): 最低NEP（直流至100 MHz） W/sqrt(Hz). Defaults to 6.99e-12.
        """
        self.Detector_Material = Detector_Material
        self.Operating_Wavelength_Range = Operating_Wavelength_Range
        self.Max_Responsivity_typ = Max_Responsivity_typ
        self.Detector_Active_Area = Detector_Active_Area
        self.RF_OUTPUT_Bandwidth = RF_OUTPUT_Bandwidth
        self.CMRR = CMRR
        self.RF_OUTPUT_Transimpedance_Gains = RF_OUTPUT_Transimpedance_Gains
        self.RF_OUTPUT_Conversion_Gain = RF_OUTPUT_Conversion_Gain
        self.CW_Saturation_Power = CW_Saturation_Power
        self.Minimum_NEP = Minimum_NEP
        
        self.iph = None # 为净光电流

    def respons_current(self, p_1_i, p_2_i):
        """输出电流功率

        Args:
            p_1_i (_type_): 端口 1 输入光信号功率
            p_2_i (_type_): 端口 1 输入光信号功率

        Returns:
            _type_: 输出电流功率
        """
        return (p_1_i + p_2_i) * self.Max_Responsivity_typ
    
    def output_power(self, p_1_i, p_2_i):
        """计算输出电信号功率

        Args:
            p_1_i (_type_): 端口 1 输入光信号功率
            p_2_i (_type_): 端口 1 输入光信号功率

        Returns:
            _type_: _description_
        """
        self.iph = self.respons_current(p_1_i, p_2_i)
        return self.RF_OUTPUT_Conversion_Gain * self.iph
