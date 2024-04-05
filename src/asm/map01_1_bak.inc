cells:
; cell label: obj_id map_x map_y,render routine address
; MIND THE LITTLE-ENDIANESS IN THE COORDINATES!!!111
cell_000: dl 0x1D0000,rend_000; cell_id 0x00 : coords 00,00 : 0x00,0x00 
cell_001: dl 0x1D0100,rend_001; cell_id 0x01 : coords 01,00 : 0x01,0x00 
cell_002: dl 0x1D0200,rend_002; cell_id 0x02 : coords 02,00 : 0x02,0x00 
cell_003: dl 0x1D0300,rend_003; cell_id 0x03 : coords 03,00 : 0x03,0x00 
cell_004: dl 0x1D0400,rend_004; cell_id 0x04 : coords 04,00 : 0x04,0x00 
cell_005: dl 0x1D0500,rend_005; cell_id 0x05 : coords 05,00 : 0x05,0x00 
cell_006: dl 0x1D0600,rend_006; cell_id 0x06 : coords 06,00 : 0x06,0x00 
cell_007: dl 0x1D0700,rend_007; cell_id 0x07 : coords 07,00 : 0x07,0x00 
cell_008: dl 0x110800,rend_008; cell_id 0x08 : coords 08,00 : 0x08,0x00 
cell_009: dl 0x1D0900,rend_009; cell_id 0x09 : coords 09,00 : 0x09,0x00 
cell_010: dl 0x1D0A00,rend_010; cell_id 0x0A : coords 10,00 : 0x0A,0x00 
cell_011: dl 0x1D0B00,rend_011; cell_id 0x0B : coords 11,00 : 0x0B,0x00 
cell_012: dl 0x1D0C00,rend_012; cell_id 0x0C : coords 12,00 : 0x0C,0x00 
cell_013: dl 0x1D0D00,rend_013; cell_id 0x0D : coords 13,00 : 0x0D,0x00 
cell_014: dl 0x0A0E00,rend_014; cell_id 0x0E : coords 14,00 : 0x0E,0x00 
cell_015: dl 0x1D0F00,rend_015; cell_id 0x0F : coords 15,00 : 0x0F,0x00 
cell_016: dl 0x1D0001,rend_016; cell_id 0x10 : coords 00,01 : 0x00,0x01 
cell_017: dl 0x1D0101,rend_017; cell_id 0x11 : coords 01,01 : 0x01,0x01 
cell_018: dl 0x1D0201,rend_018; cell_id 0x12 : coords 02,01 : 0x02,0x01 
cell_019: dl 0x1D0301,rend_019; cell_id 0x13 : coords 03,01 : 0x03,0x01 
cell_020: dl 0x1D0401,rend_020; cell_id 0x14 : coords 04,01 : 0x04,0x01 
cell_021: dl 0x1D0501,rend_021; cell_id 0x15 : coords 05,01 : 0x05,0x01 
cell_022: dl 0x1D0601,rend_022; cell_id 0x16 : coords 06,01 : 0x06,0x01 
cell_023: dl 0x1D0701,rend_023; cell_id 0x17 : coords 07,01 : 0x07,0x01 
cell_024: dl 0x0A0801,rend_024; cell_id 0x18 : coords 08,01 : 0x08,0x01 
cell_025: dl 0x1D0901,rend_025; cell_id 0x19 : coords 09,01 : 0x09,0x01 
cell_026: dl 0x1D0A01,rend_026; cell_id 0x1A : coords 10,01 : 0x0A,0x01 
cell_027: dl 0x1D0B01,rend_027; cell_id 0x1B : coords 11,01 : 0x0B,0x01 
cell_028: dl 0x1D0C01,rend_028; cell_id 0x1C : coords 12,01 : 0x0C,0x01 
cell_029: dl 0x1D0D01,rend_029; cell_id 0x1D : coords 13,01 : 0x0D,0x01 
cell_030: dl 0x1E0E01,rend_030; cell_id 0x1E : coords 14,01 : 0x0E,0x01 
cell_031: dl 0x1D0F01,rend_031; cell_id 0x1F : coords 15,01 : 0x0F,0x01 
cell_032: dl 0x1D0002,rend_032; cell_id 0x20 : coords 00,02 : 0x00,0x02 
cell_033: dl 0x1D0102,rend_033; cell_id 0x21 : coords 01,02 : 0x01,0x02 
cell_034: dl 0x1D0202,rend_034; cell_id 0x22 : coords 02,02 : 0x02,0x02 
cell_035: dl 0x0E0302,rend_035; cell_id 0x23 : coords 03,02 : 0x03,0x02 
cell_036: dl 0x0E0402,rend_036; cell_id 0x24 : coords 04,02 : 0x04,0x02 
cell_037: dl 0x1D0502,rend_037; cell_id 0x25 : coords 05,02 : 0x05,0x02 
cell_038: dl 0x110602,rend_038; cell_id 0x26 : coords 06,02 : 0x06,0x02 
cell_039: dl 0x0A0702,rend_039; cell_id 0x27 : coords 07,02 : 0x07,0x02 
cell_040: dl 0x110802,rend_040; cell_id 0x28 : coords 08,02 : 0x08,0x02 
cell_041: dl 0x1D0902,rend_041; cell_id 0x29 : coords 09,02 : 0x09,0x02 
cell_042: dl 0x1D0A02,rend_042; cell_id 0x2A : coords 10,02 : 0x0A,0x02 
cell_043: dl 0x1D0B02,rend_043; cell_id 0x2B : coords 11,02 : 0x0B,0x02 
cell_044: dl 0x1D0C02,rend_044; cell_id 0x2C : coords 12,02 : 0x0C,0x02 
cell_045: dl 0x1D0D02,rend_045; cell_id 0x2D : coords 13,02 : 0x0D,0x02 
cell_046: dl 0x0A0E02,rend_046; cell_id 0x2E : coords 14,02 : 0x0E,0x02 
cell_047: dl 0x1D0F02,rend_047; cell_id 0x2F : coords 15,02 : 0x0F,0x02 
cell_048: dl 0x1D0003,rend_048; cell_id 0x30 : coords 00,03 : 0x00,0x03 
cell_049: dl 0x1D0103,rend_049; cell_id 0x31 : coords 01,03 : 0x01,0x03 
cell_050: dl 0x3A0203,rend_050; cell_id 0x32 : coords 02,03 : 0x02,0x03 
cell_051: dl 0x1D0303,rend_051; cell_id 0x33 : coords 03,03 : 0x03,0x03 
cell_052: dl 0x1D0403,rend_052; cell_id 0x34 : coords 04,03 : 0x04,0x03 
cell_053: dl 0x3B0503,rend_053; cell_id 0x35 : coords 05,03 : 0x05,0x03 
cell_054: dl 0x1D0603,rend_054; cell_id 0x36 : coords 06,03 : 0x06,0x03 
cell_055: dl 0x1D0703,rend_055; cell_id 0x37 : coords 07,03 : 0x07,0x03 
cell_056: dl 0x390803,rend_056; cell_id 0x38 : coords 08,03 : 0x08,0x03 
cell_057: dl 0x1D0903,rend_057; cell_id 0x39 : coords 09,03 : 0x09,0x03 
cell_058: dl 0x1D0A03,rend_058; cell_id 0x3A : coords 10,03 : 0x0A,0x03 
cell_059: dl 0x1D0B03,rend_059; cell_id 0x3B : coords 11,03 : 0x0B,0x03 
cell_060: dl 0x1D0C03,rend_060; cell_id 0x3C : coords 12,03 : 0x0C,0x03 
cell_061: dl 0x1D0D03,rend_061; cell_id 0x3D : coords 13,03 : 0x0D,0x03 
cell_062: dl 0x110E03,rend_062; cell_id 0x3E : coords 14,03 : 0x0E,0x03 
cell_063: dl 0x1D0F03,rend_063; cell_id 0x3F : coords 15,03 : 0x0F,0x03 
cell_064: dl 0x1D0004,rend_064; cell_id 0x40 : coords 00,04 : 0x00,0x04 
cell_065: dl 0x1D0104,rend_065; cell_id 0x41 : coords 01,04 : 0x01,0x04 
cell_066: dl 0x1D0204,rend_066; cell_id 0x42 : coords 02,04 : 0x02,0x04 
cell_067: dl 0x0E0304,rend_067; cell_id 0x43 : coords 03,04 : 0x03,0x04 
cell_068: dl 0x0E0404,rend_068; cell_id 0x44 : coords 04,04 : 0x04,0x04 
cell_069: dl 0x1D0504,rend_069; cell_id 0x45 : coords 05,04 : 0x05,0x04 
cell_070: dl 0x110604,rend_070; cell_id 0x46 : coords 06,04 : 0x06,0x04 
cell_071: dl 0x0A0704,rend_071; cell_id 0x47 : coords 07,04 : 0x07,0x04 
cell_072: dl 0x110804,rend_072; cell_id 0x48 : coords 08,04 : 0x08,0x04 
cell_073: dl 0x1D0904,rend_073; cell_id 0x49 : coords 09,04 : 0x09,0x04 
cell_074: dl 0x1D0A04,rend_074; cell_id 0x4A : coords 10,04 : 0x0A,0x04 
cell_075: dl 0x1D0B04,rend_075; cell_id 0x4B : coords 11,04 : 0x0B,0x04 
cell_076: dl 0x1D0C04,rend_076; cell_id 0x4C : coords 12,04 : 0x0C,0x04 
cell_077: dl 0x1D0D04,rend_077; cell_id 0x4D : coords 13,04 : 0x0D,0x04 
cell_078: dl 0x0A0E04,rend_078; cell_id 0x4E : coords 14,04 : 0x0E,0x04 
cell_079: dl 0x1D0F04,rend_079; cell_id 0x4F : coords 15,04 : 0x0F,0x04 
cell_080: dl 0x1D0005,rend_080; cell_id 0x50 : coords 00,05 : 0x00,0x05 
cell_081: dl 0x1D0105,rend_081; cell_id 0x51 : coords 01,05 : 0x01,0x05 
cell_082: dl 0x1D0205,rend_082; cell_id 0x52 : coords 02,05 : 0x02,0x05 
cell_083: dl 0x1D0305,rend_083; cell_id 0x53 : coords 03,05 : 0x03,0x05 
cell_084: dl 0x1D0405,rend_084; cell_id 0x54 : coords 04,05 : 0x04,0x05 
cell_085: dl 0x1D0505,rend_085; cell_id 0x55 : coords 05,05 : 0x05,0x05 
cell_086: dl 0x1D0605,rend_086; cell_id 0x56 : coords 06,05 : 0x06,0x05 
cell_087: dl 0x1D0705,rend_087; cell_id 0x57 : coords 07,05 : 0x07,0x05 
cell_088: dl 0x1D0805,rend_088; cell_id 0x58 : coords 08,05 : 0x08,0x05 
cell_089: dl 0x110905,rend_089; cell_id 0x59 : coords 09,05 : 0x09,0x05 
cell_090: dl 0x0A0A05,rend_090; cell_id 0x5A : coords 10,05 : 0x0A,0x05 
cell_091: dl 0x110B05,rend_091; cell_id 0x5B : coords 11,05 : 0x0B,0x05 
cell_092: dl 0x0A0C05,rend_092; cell_id 0x5C : coords 12,05 : 0x0C,0x05 
cell_093: dl 0x110D05,rend_093; cell_id 0x5D : coords 13,05 : 0x0D,0x05 
cell_094: dl 0x1D0E05,rend_094; cell_id 0x5E : coords 14,05 : 0x0E,0x05 
cell_095: dl 0x1D0F05,rend_095; cell_id 0x5F : coords 15,05 : 0x0F,0x05 
cell_096: dl 0x1D0006,rend_096; cell_id 0x60 : coords 00,06 : 0x00,0x06 
cell_097: dl 0x1D0106,rend_097; cell_id 0x61 : coords 01,06 : 0x01,0x06 
cell_098: dl 0x1D0206,rend_098; cell_id 0x62 : coords 02,06 : 0x02,0x06 
cell_099: dl 0x1D0306,rend_099; cell_id 0x63 : coords 03,06 : 0x03,0x06 
cell_100: dl 0x1D0406,rend_100; cell_id 0x64 : coords 04,06 : 0x04,0x06 
cell_101: dl 0x1D0506,rend_101; cell_id 0x65 : coords 05,06 : 0x05,0x06 
cell_102: dl 0x1D0606,rend_102; cell_id 0x66 : coords 06,06 : 0x06,0x06 
cell_103: dl 0x1D0706,rend_103; cell_id 0x67 : coords 07,06 : 0x07,0x06 
cell_104: dl 0x1D0806,rend_104; cell_id 0x68 : coords 08,06 : 0x08,0x06 
cell_105: dl 0x1D0906,rend_105; cell_id 0x69 : coords 09,06 : 0x09,0x06 
cell_106: dl 0x1D0A06,rend_106; cell_id 0x6A : coords 10,06 : 0x0A,0x06 
cell_107: dl 0x1D0B06,rend_107; cell_id 0x6B : coords 11,06 : 0x0B,0x06 
cell_108: dl 0x1D0C06,rend_108; cell_id 0x6C : coords 12,06 : 0x0C,0x06 
cell_109: dl 0x1D0D06,rend_109; cell_id 0x6D : coords 13,06 : 0x0D,0x06 
cell_110: dl 0x1D0E06,rend_110; cell_id 0x6E : coords 14,06 : 0x0E,0x06 
cell_111: dl 0x1D0F06,rend_111; cell_id 0x6F : coords 15,06 : 0x0F,0x06 
cell_112: dl 0x1D0007,rend_112; cell_id 0x70 : coords 00,07 : 0x00,0x07 
cell_113: dl 0x1D0107,rend_113; cell_id 0x71 : coords 01,07 : 0x01,0x07 
cell_114: dl 0x1D0207,rend_114; cell_id 0x72 : coords 02,07 : 0x02,0x07 
cell_115: dl 0x1D0307,rend_115; cell_id 0x73 : coords 03,07 : 0x03,0x07 
cell_116: dl 0x1D0407,rend_116; cell_id 0x74 : coords 04,07 : 0x04,0x07 
cell_117: dl 0x1D0507,rend_117; cell_id 0x75 : coords 05,07 : 0x05,0x07 
cell_118: dl 0x1D0607,rend_118; cell_id 0x76 : coords 06,07 : 0x06,0x07 
cell_119: dl 0x1D0707,rend_119; cell_id 0x77 : coords 07,07 : 0x07,0x07 
cell_120: dl 0x1D0807,rend_120; cell_id 0x78 : coords 08,07 : 0x08,0x07 
cell_121: dl 0x1D0907,rend_121; cell_id 0x79 : coords 09,07 : 0x09,0x07 
cell_122: dl 0x1D0A07,rend_122; cell_id 0x7A : coords 10,07 : 0x0A,0x07 
cell_123: dl 0x1D0B07,rend_123; cell_id 0x7B : coords 11,07 : 0x0B,0x07 
cell_124: dl 0x1D0C07,rend_124; cell_id 0x7C : coords 12,07 : 0x0C,0x07 
cell_125: dl 0x1D0D07,rend_125; cell_id 0x7D : coords 13,07 : 0x0D,0x07 
cell_126: dl 0x1D0E07,rend_126; cell_id 0x7E : coords 14,07 : 0x0E,0x07 
cell_127: dl 0x1D0F07,rend_127; cell_id 0x7F : coords 15,07 : 0x0F,0x07 
cell_128: dl 0x1D0008,rend_128; cell_id 0x80 : coords 00,08 : 0x00,0x08 
cell_129: dl 0x1D0108,rend_129; cell_id 0x81 : coords 01,08 : 0x01,0x08 
cell_130: dl 0x1D0208,rend_130; cell_id 0x82 : coords 02,08 : 0x02,0x08 
cell_131: dl 0x1D0308,rend_131; cell_id 0x83 : coords 03,08 : 0x03,0x08 
cell_132: dl 0x1D0408,rend_132; cell_id 0x84 : coords 04,08 : 0x04,0x08 
cell_133: dl 0x1D0508,rend_133; cell_id 0x85 : coords 05,08 : 0x05,0x08 
cell_134: dl 0x1D0608,rend_134; cell_id 0x86 : coords 06,08 : 0x06,0x08 
cell_135: dl 0x1D0708,rend_135; cell_id 0x87 : coords 07,08 : 0x07,0x08 
cell_136: dl 0x1D0808,rend_136; cell_id 0x88 : coords 08,08 : 0x08,0x08 
cell_137: dl 0x1D0908,rend_137; cell_id 0x89 : coords 09,08 : 0x09,0x08 
cell_138: dl 0x1D0A08,rend_138; cell_id 0x8A : coords 10,08 : 0x0A,0x08 
cell_139: dl 0x1D0B08,rend_139; cell_id 0x8B : coords 11,08 : 0x0B,0x08 
cell_140: dl 0x1D0C08,rend_140; cell_id 0x8C : coords 12,08 : 0x0C,0x08 
cell_141: dl 0x1D0D08,rend_141; cell_id 0x8D : coords 13,08 : 0x0D,0x08 
cell_142: dl 0x1D0E08,rend_142; cell_id 0x8E : coords 14,08 : 0x0E,0x08 
cell_143: dl 0x1D0F08,rend_143; cell_id 0x8F : coords 15,08 : 0x0F,0x08 
cell_144: dl 0x1D0009,rend_144; cell_id 0x90 : coords 00,09 : 0x00,0x09 
cell_145: dl 0x1D0109,rend_145; cell_id 0x91 : coords 01,09 : 0x01,0x09 
cell_146: dl 0x1D0209,rend_146; cell_id 0x92 : coords 02,09 : 0x02,0x09 
cell_147: dl 0x1D0309,rend_147; cell_id 0x93 : coords 03,09 : 0x03,0x09 
cell_148: dl 0x1D0409,rend_148; cell_id 0x94 : coords 04,09 : 0x04,0x09 
cell_149: dl 0x1D0509,rend_149; cell_id 0x95 : coords 05,09 : 0x05,0x09 
cell_150: dl 0x1D0609,rend_150; cell_id 0x96 : coords 06,09 : 0x06,0x09 
cell_151: dl 0x1D0709,rend_151; cell_id 0x97 : coords 07,09 : 0x07,0x09 
cell_152: dl 0x1D0809,rend_152; cell_id 0x98 : coords 08,09 : 0x08,0x09 
cell_153: dl 0x1D0909,rend_153; cell_id 0x99 : coords 09,09 : 0x09,0x09 
cell_154: dl 0x1D0A09,rend_154; cell_id 0x9A : coords 10,09 : 0x0A,0x09 
cell_155: dl 0x1D0B09,rend_155; cell_id 0x9B : coords 11,09 : 0x0B,0x09 
cell_156: dl 0x1D0C09,rend_156; cell_id 0x9C : coords 12,09 : 0x0C,0x09 
cell_157: dl 0x1D0D09,rend_157; cell_id 0x9D : coords 13,09 : 0x0D,0x09 
cell_158: dl 0x1D0E09,rend_158; cell_id 0x9E : coords 14,09 : 0x0E,0x09 
cell_159: dl 0x1D0F09,rend_159; cell_id 0x9F : coords 15,09 : 0x0F,0x09 
cell_160: dl 0x1D000A,rend_160; cell_id 0xA0 : coords 00,10 : 0x00,0x0A 
cell_161: dl 0x1D010A,rend_161; cell_id 0xA1 : coords 01,10 : 0x01,0x0A 
cell_162: dl 0x1D020A,rend_162; cell_id 0xA2 : coords 02,10 : 0x02,0x0A 
cell_163: dl 0x1D030A,rend_163; cell_id 0xA3 : coords 03,10 : 0x03,0x0A 
cell_164: dl 0x1D040A,rend_164; cell_id 0xA4 : coords 04,10 : 0x04,0x0A 
cell_165: dl 0x1D050A,rend_165; cell_id 0xA5 : coords 05,10 : 0x05,0x0A 
cell_166: dl 0x1D060A,rend_166; cell_id 0xA6 : coords 06,10 : 0x06,0x0A 
cell_167: dl 0x1D070A,rend_167; cell_id 0xA7 : coords 07,10 : 0x07,0x0A 
cell_168: dl 0x1D080A,rend_168; cell_id 0xA8 : coords 08,10 : 0x08,0x0A 
cell_169: dl 0x1D090A,rend_169; cell_id 0xA9 : coords 09,10 : 0x09,0x0A 
cell_170: dl 0x1D0A0A,rend_170; cell_id 0xAA : coords 10,10 : 0x0A,0x0A 
cell_171: dl 0x1D0B0A,rend_171; cell_id 0xAB : coords 11,10 : 0x0B,0x0A 
cell_172: dl 0x1D0C0A,rend_172; cell_id 0xAC : coords 12,10 : 0x0C,0x0A 
cell_173: dl 0x1D0D0A,rend_173; cell_id 0xAD : coords 13,10 : 0x0D,0x0A 
cell_174: dl 0x1D0E0A,rend_174; cell_id 0xAE : coords 14,10 : 0x0E,0x0A 
cell_175: dl 0x1D0F0A,rend_175; cell_id 0xAF : coords 15,10 : 0x0F,0x0A 
cell_176: dl 0x1D000B,rend_176; cell_id 0xB0 : coords 00,11 : 0x00,0x0B 
cell_177: dl 0x1D010B,rend_177; cell_id 0xB1 : coords 01,11 : 0x01,0x0B 
cell_178: dl 0x1D020B,rend_178; cell_id 0xB2 : coords 02,11 : 0x02,0x0B 
cell_179: dl 0x1D030B,rend_179; cell_id 0xB3 : coords 03,11 : 0x03,0x0B 
cell_180: dl 0x1D040B,rend_180; cell_id 0xB4 : coords 04,11 : 0x04,0x0B 
cell_181: dl 0x1D050B,rend_181; cell_id 0xB5 : coords 05,11 : 0x05,0x0B 
cell_182: dl 0x1D060B,rend_182; cell_id 0xB6 : coords 06,11 : 0x06,0x0B 
cell_183: dl 0x1D070B,rend_183; cell_id 0xB7 : coords 07,11 : 0x07,0x0B 
cell_184: dl 0x1D080B,rend_184; cell_id 0xB8 : coords 08,11 : 0x08,0x0B 
cell_185: dl 0x1D090B,rend_185; cell_id 0xB9 : coords 09,11 : 0x09,0x0B 
cell_186: dl 0x1D0A0B,rend_186; cell_id 0xBA : coords 10,11 : 0x0A,0x0B 
cell_187: dl 0x1D0B0B,rend_187; cell_id 0xBB : coords 11,11 : 0x0B,0x0B 
cell_188: dl 0x1D0C0B,rend_188; cell_id 0xBC : coords 12,11 : 0x0C,0x0B 
cell_189: dl 0x1D0D0B,rend_189; cell_id 0xBD : coords 13,11 : 0x0D,0x0B 
cell_190: dl 0x1D0E0B,rend_190; cell_id 0xBE : coords 14,11 : 0x0E,0x0B 
cell_191: dl 0x1D0F0B,rend_191; cell_id 0xBF : coords 15,11 : 0x0F,0x0B 
cell_192: dl 0x1D000C,rend_192; cell_id 0xC0 : coords 00,12 : 0x00,0x0C 
cell_193: dl 0x1D010C,rend_193; cell_id 0xC1 : coords 01,12 : 0x01,0x0C 
cell_194: dl 0x1D020C,rend_194; cell_id 0xC2 : coords 02,12 : 0x02,0x0C 
cell_195: dl 0x1D030C,rend_195; cell_id 0xC3 : coords 03,12 : 0x03,0x0C 
cell_196: dl 0x1D040C,rend_196; cell_id 0xC4 : coords 04,12 : 0x04,0x0C 
cell_197: dl 0x1D050C,rend_197; cell_id 0xC5 : coords 05,12 : 0x05,0x0C 
cell_198: dl 0x1D060C,rend_198; cell_id 0xC6 : coords 06,12 : 0x06,0x0C 
cell_199: dl 0x1D070C,rend_199; cell_id 0xC7 : coords 07,12 : 0x07,0x0C 
cell_200: dl 0x1D080C,rend_200; cell_id 0xC8 : coords 08,12 : 0x08,0x0C 
cell_201: dl 0x1D090C,rend_201; cell_id 0xC9 : coords 09,12 : 0x09,0x0C 
cell_202: dl 0x1D0A0C,rend_202; cell_id 0xCA : coords 10,12 : 0x0A,0x0C 
cell_203: dl 0x1D0B0C,rend_203; cell_id 0xCB : coords 11,12 : 0x0B,0x0C 
cell_204: dl 0x1D0C0C,rend_204; cell_id 0xCC : coords 12,12 : 0x0C,0x0C 
cell_205: dl 0x1D0D0C,rend_205; cell_id 0xCD : coords 13,12 : 0x0D,0x0C 
cell_206: dl 0x1D0E0C,rend_206; cell_id 0xCE : coords 14,12 : 0x0E,0x0C 
cell_207: dl 0x1D0F0C,rend_207; cell_id 0xCF : coords 15,12 : 0x0F,0x0C 
cell_208: dl 0x1D000D,rend_208; cell_id 0xD0 : coords 00,13 : 0x00,0x0D 
cell_209: dl 0x1D010D,rend_209; cell_id 0xD1 : coords 01,13 : 0x01,0x0D 
cell_210: dl 0x1D020D,rend_210; cell_id 0xD2 : coords 02,13 : 0x02,0x0D 
cell_211: dl 0x1D030D,rend_211; cell_id 0xD3 : coords 03,13 : 0x03,0x0D 
cell_212: dl 0x1D040D,rend_212; cell_id 0xD4 : coords 04,13 : 0x04,0x0D 
cell_213: dl 0x1D050D,rend_213; cell_id 0xD5 : coords 05,13 : 0x05,0x0D 
cell_214: dl 0x1D060D,rend_214; cell_id 0xD6 : coords 06,13 : 0x06,0x0D 
cell_215: dl 0x1D070D,rend_215; cell_id 0xD7 : coords 07,13 : 0x07,0x0D 
cell_216: dl 0x1D080D,rend_216; cell_id 0xD8 : coords 08,13 : 0x08,0x0D 
cell_217: dl 0x1D090D,rend_217; cell_id 0xD9 : coords 09,13 : 0x09,0x0D 
cell_218: dl 0x1D0A0D,rend_218; cell_id 0xDA : coords 10,13 : 0x0A,0x0D 
cell_219: dl 0x1D0B0D,rend_219; cell_id 0xDB : coords 11,13 : 0x0B,0x0D 
cell_220: dl 0x1D0C0D,rend_220; cell_id 0xDC : coords 12,13 : 0x0C,0x0D 
cell_221: dl 0x1D0D0D,rend_221; cell_id 0xDD : coords 13,13 : 0x0D,0x0D 
cell_222: dl 0x1D0E0D,rend_222; cell_id 0xDE : coords 14,13 : 0x0E,0x0D 
cell_223: dl 0x1D0F0D,rend_223; cell_id 0xDF : coords 15,13 : 0x0F,0x0D 
cell_224: dl 0x1D000E,rend_224; cell_id 0xE0 : coords 00,14 : 0x00,0x0E 
cell_225: dl 0x1D010E,rend_225; cell_id 0xE1 : coords 01,14 : 0x01,0x0E 
cell_226: dl 0x1D020E,rend_226; cell_id 0xE2 : coords 02,14 : 0x02,0x0E 
cell_227: dl 0x1D030E,rend_227; cell_id 0xE3 : coords 03,14 : 0x03,0x0E 
cell_228: dl 0x1D040E,rend_228; cell_id 0xE4 : coords 04,14 : 0x04,0x0E 
cell_229: dl 0x1D050E,rend_229; cell_id 0xE5 : coords 05,14 : 0x05,0x0E 
cell_230: dl 0x1D060E,rend_230; cell_id 0xE6 : coords 06,14 : 0x06,0x0E 
cell_231: dl 0x1D070E,rend_231; cell_id 0xE7 : coords 07,14 : 0x07,0x0E 
cell_232: dl 0x1D080E,rend_232; cell_id 0xE8 : coords 08,14 : 0x08,0x0E 
cell_233: dl 0x1D090E,rend_233; cell_id 0xE9 : coords 09,14 : 0x09,0x0E 
cell_234: dl 0x1D0A0E,rend_234; cell_id 0xEA : coords 10,14 : 0x0A,0x0E 
cell_235: dl 0x1D0B0E,rend_235; cell_id 0xEB : coords 11,14 : 0x0B,0x0E 
cell_236: dl 0x1D0C0E,rend_236; cell_id 0xEC : coords 12,14 : 0x0C,0x0E 
cell_237: dl 0x1D0D0E,rend_237; cell_id 0xED : coords 13,14 : 0x0D,0x0E 
cell_238: dl 0x1D0E0E,rend_238; cell_id 0xEE : coords 14,14 : 0x0E,0x0E 
cell_239: dl 0x1D0F0E,rend_239; cell_id 0xEF : coords 15,14 : 0x0F,0x0E 
cell_240: dl 0x1D000F,rend_240; cell_id 0xF0 : coords 00,15 : 0x00,0x0F 
cell_241: dl 0x1D010F,rend_241; cell_id 0xF1 : coords 01,15 : 0x01,0x0F 
cell_242: dl 0x1D020F,rend_242; cell_id 0xF2 : coords 02,15 : 0x02,0x0F 
cell_243: dl 0x1D030F,rend_243; cell_id 0xF3 : coords 03,15 : 0x03,0x0F 
cell_244: dl 0x1D040F,rend_244; cell_id 0xF4 : coords 04,15 : 0x04,0x0F 
cell_245: dl 0x1D050F,rend_245; cell_id 0xF5 : coords 05,15 : 0x05,0x0F 
cell_246: dl 0x1D060F,rend_246; cell_id 0xF6 : coords 06,15 : 0x06,0x0F 
cell_247: dl 0x1D070F,rend_247; cell_id 0xF7 : coords 07,15 : 0x07,0x0F 
cell_248: dl 0x1D080F,rend_248; cell_id 0xF8 : coords 08,15 : 0x08,0x0F 
cell_249: dl 0x1D090F,rend_249; cell_id 0xF9 : coords 09,15 : 0x09,0x0F 
cell_250: dl 0x1D0A0F,rend_250; cell_id 0xFA : coords 10,15 : 0x0A,0x0F 
cell_251: dl 0x1D0B0F,rend_251; cell_id 0xFB : coords 11,15 : 0x0B,0x0F 
cell_252: dl 0x1D0C0F,rend_252; cell_id 0xFC : coords 12,15 : 0x0C,0x0F 
cell_253: dl 0x1D0D0F,rend_253; cell_id 0xFD : coords 13,15 : 0x0D,0x0F 
cell_254: dl 0x1D0E0F,rend_254; cell_id 0xFE : coords 14,15 : 0x0E,0x0F 
cell_255: dl 0x1D0F0F,rend_255; cell_id 0xFF : coords 15,15 : 0x0F,0x0F 
; room1 render routines:
; 0x00 : 00,00 : 0x00,0x00 
rend_000: dl rend_000_0,rend_000_1,rend_000_2,rend_000_3
rend_000_0:
	jp render_scene_return
rend_000_1:
	jp render_scene_return
rend_000_2:
	ld hl,0x150199 ; BUF_14_21
	call render_panel
	ld hl,0x1C019F ; BUF_14_30
	call render_panel
	ld hl,0x2301A1 ; BUF_14_35
	call render_panel
	ld hl,0x2801A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_000_3:
	jp render_scene_return
; 0x01 : 01,00 : 0x01,0x00 
rend_001: dl rend_001_0,rend_001_1,rend_001_2,rend_001_3
rend_001_0:
	jp render_scene_return
rend_001_1:
	ld hl,0x3001AA ; BUF_14_48
	call render_panel
	jp render_scene_return
rend_001_2:
	ld hl,0x0301F8 ; BUF_17_03
	call render_panel
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x2301A1 ; BUF_14_35
	call render_panel
	ld hl,0x2D01A7 ; BUF_14_45
	call render_panel
	jp render_scene_return
rend_001_3:
	jp render_scene_return
; 0x02 : 02,00 : 0x02,0x00 
rend_002: dl rend_002_0,rend_002_1,rend_002_2,rend_002_3
rend_002_0:
	jp render_scene_return
rend_002_1:
	ld hl,0x2F01A9 ; BUF_14_47
	call render_panel
	ld hl,0x3301AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_002_2:
	ld hl,0x030103 ; BUF_10_03
	call render_panel
	ld hl,0x150202 ; BUF_17_21
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x2D01A7 ; BUF_14_45
	call render_panel
	jp render_scene_return
rend_002_3:
	jp render_scene_return
; 0x03 : 03,00 : 0x03,0x00 
rend_003: dl rend_003_0,rend_003_1,rend_003_2,rend_003_3
rend_003_0:
	jp render_scene_return
rend_003_1:
	ld hl,0x3201AB ; BUF_14_50
	call render_panel
	ld hl,0x3301AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_003_2:
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x15010D ; BUF_10_21
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x23020A ; BUF_17_35
	call render_panel
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	jp render_scene_return
rend_003_3:
	jp render_scene_return
; 0x04 : 04,00 : 0x04,0x00 
rend_004: dl rend_004_0,rend_004_1,rend_004_2,rend_004_3
rend_004_0:
	jp render_scene_return
rend_004_1:
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	ld hl,0x3101AB ; BUF_14_50
	call render_panel
	ld hl,0x3201AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_004_2:
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x230115 ; BUF_10_35
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_004_3:
	jp render_scene_return
; 0x05 : 05,00 : 0x05,0x00 
rend_005: dl rend_005_0,rend_005_1,rend_005_2,rend_005_3
rend_005_0:
	ld hl,0x3001AA ; BUF_14_48
	call render_panel
	jp render_scene_return
rend_005_1:
	ld hl,0x2E01A8 ; BUF_14_46
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x3101AB ; BUF_14_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_005_2:
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2D011B ; BUF_10_45
	call render_panel
	jp render_scene_return
rend_005_3:
	jp render_scene_return
; 0x06 : 06,00 : 0x06,0x00 
rend_006: dl rend_006_0,rend_006_1,rend_006_2,rend_006_3
rend_006_0:
	ld hl,0x2601A4 ; BUF_14_38
	call render_panel
	ld hl,0x3001AA ; BUF_14_48
	call render_panel
	jp render_scene_return
rend_006_1:
	ld hl,0x2D01A7 ; BUF_14_45
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	jp render_scene_return
rend_006_2:
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_006_3:
	jp render_scene_return
; 0x07 : 07,00 : 0x07,0x00 
rend_007: dl rend_007_0,rend_007_1,rend_007_2,rend_007_3
rend_007_0:
	ld hl,0x18019C ; BUF_14_24
	call render_panel
	ld hl,0x2601A4 ; BUF_14_38
	call render_panel
	ld hl,0x2C01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_007_1:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_007_2:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_007_3:
	jp render_scene_return
; 0x08 : 08,00 : 0x08,0x00 
rend_008:
; 0x09 : 09,00 : 0x09,0x00 
rend_009: dl rend_009_0,rend_009_1,rend_009_2,rend_009_3
rend_009_0:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_009_1:
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x11010A ; BUF_10_14
	call render_panel
	ld hl,0x1201FF ; BUF_17_14
	call render_panel
	ld hl,0x160203 ; BUF_17_22
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_009_2:
	ld hl,0x0A010A ; BUF_10_14
	call render_panel
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x0C010A ; BUF_10_14
	call render_panel
	ld hl,0x0D0222 ; BUF_30_14
	call render_panel
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	jp render_scene_return
rend_009_3:
	jp render_scene_return
; 0x0A : 10,00 : 0x0A,0x00 
rend_010: dl rend_010_0,rend_010_1,rend_010_2,rend_010_3
rend_010_0:
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	jp render_scene_return
rend_010_1:
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x10010A ; BUF_10_14
	call render_panel
	ld hl,0x1101FF ; BUF_17_14
	call render_panel
	ld hl,0x150202 ; BUF_17_21
	call render_panel
	ld hl,0x1A0112 ; BUF_10_26
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_010_2:
	ld hl,0x1B0208 ; BUF_17_30
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x1D022B ; BUF_30_30
	call render_panel
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	jp render_scene_return
rend_010_3:
	jp render_scene_return
; 0x0B : 11,00 : 0x0B,0x00 
rend_011: dl rend_011_0,rend_011_1,rend_011_2,rend_011_3
rend_011_0:
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	jp render_scene_return
rend_011_1:
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x140201 ; BUF_17_20
	call render_panel
	ld hl,0x190111 ; BUF_10_25
	call render_panel
	ld hl,0x27020E ; BUF_17_39
	call render_panel
	jp render_scene_return
rend_011_2:
	ld hl,0x28011A ; BUF_10_42
	call render_panel
	ld hl,0x290232 ; BUF_30_42
	call render_panel
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	jp render_scene_return
rend_011_3:
	jp render_scene_return
; 0x0C : 12,00 : 0x0C,0x00 
rend_012: dl rend_012_0,rend_012_1,rend_012_2,rend_012_3
rend_012_0:
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	jp render_scene_return
rend_012_1:
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x0C010A ; BUF_10_14
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x130200 ; BUF_17_19
	call render_panel
	ld hl,0x180110 ; BUF_10_24
	call render_panel
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x30011E ; BUF_10_48
	call render_panel
	jp render_scene_return
rend_012_2:
	ld hl,0x310237 ; BUF_30_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	jp render_scene_return
rend_012_3:
	jp render_scene_return
; 0x0D : 13,00 : 0x0D,0x00 
rend_013: dl rend_013_0,rend_013_1,rend_013_2,rend_013_3
rend_013_0:
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x1201FF ; BUF_17_14
	call render_panel
	jp render_scene_return
rend_013_1:
	ld hl,0x0A01FF ; BUF_17_14
	call render_panel
	ld hl,0x0B010A ; BUF_10_14
	call render_panel
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x17010F ; BUF_10_23
	call render_panel
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350239 ; BUF_30_53
	call render_panel
	jp render_scene_return
rend_013_2:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_013_3:
	jp render_scene_return
; 0x0E : 14,00 : 0x0E,0x00 
rend_014:
; 0x0F : 15,00 : 0x0F,0x00 
rend_015: dl rend_015_0,rend_015_1,rend_015_2,rend_015_3
rend_015_0:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_015_1:
	ld hl,0x16010E ; BUF_10_22
	call render_panel
	ld hl,0x24020B ; BUF_17_36
	call render_panel
	ld hl,0x2E011C ; BUF_10_46
	call render_panel
	ld hl,0x340238 ; BUF_30_52
	call render_panel
	jp render_scene_return
rend_015_2:
	jp render_scene_return
rend_015_3:
	jp render_scene_return
; 0x10 : 00,01 : 0x00,0x01 
rend_016: dl rend_016_0,rend_016_1,rend_016_2,rend_016_3
rend_016_0:
	jp render_scene_return
rend_016_1:
	jp render_scene_return
rend_016_2:
	ld hl,0x16019A ; BUF_14_22
	call render_panel
	ld hl,0x2401A2 ; BUF_14_36
	call render_panel
	ld hl,0x2901A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_016_3:
	jp render_scene_return
; 0x11 : 01,01 : 0x01,0x01 
rend_017: dl rend_017_0,rend_017_1,rend_017_2,rend_017_3
rend_017_0:
	jp render_scene_return
rend_017_1:
	jp render_scene_return
rend_017_2:
	ld hl,0x0401F9 ; BUF_17_04
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x2401A2 ; BUF_14_36
	call render_panel
	ld hl,0x2E01A8 ; BUF_14_46
	call render_panel
	ld hl,0x3101AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_017_3:
	jp render_scene_return
; 0x12 : 02,01 : 0x02,0x01 
rend_018: dl rend_018_0,rend_018_1,rend_018_2,rend_018_3
rend_018_0:
	jp render_scene_return
rend_018_1:
	ld hl,0x3501AD ; BUF_14_53
	call render_panel
	jp render_scene_return
rend_018_2:
	ld hl,0x040104 ; BUF_10_04
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x160203 ; BUF_17_22
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x2E01A8 ; BUF_14_46
	call render_panel
	ld hl,0x3401AC ; BUF_14_52
	call render_panel
	jp render_scene_return
rend_018_3:
	jp render_scene_return
; 0x13 : 03,01 : 0x03,0x01 
rend_019: dl rend_019_0,rend_019_1,rend_019_2,rend_019_3
rend_019_0:
	jp render_scene_return
rend_019_1:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
rend_019_2:
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x16010E ; BUF_10_22
	call render_panel
	ld hl,0x24020B ; BUF_17_36
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x3401AC ; BUF_14_52
	call render_panel
	jp render_scene_return
rend_019_3:
	jp render_scene_return
; 0x14 : 04,01 : 0x04,0x01 
rend_020: dl rend_020_0,rend_020_1,rend_020_2,rend_020_3
rend_020_0:
	ld hl,0x3501AD ; BUF_14_53
	call render_panel
	jp render_scene_return
rend_020_1:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
rend_020_2:
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x240116 ; BUF_10_36
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_020_3:
	jp render_scene_return
; 0x15 : 05,01 : 0x05,0x01 
rend_021: dl rend_021_0,rend_021_1,rend_021_2,rend_021_3
rend_021_0:
	ld hl,0x2F01A9 ; BUF_14_47
	call render_panel
	ld hl,0x3501AD ; BUF_14_53
	call render_panel
	jp render_scene_return
rend_021_1:
	ld hl,0x3401AC ; BUF_14_52
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_021_2:
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x2E011C ; BUF_10_46
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_021_3:
	jp render_scene_return
; 0x16 : 06,01 : 0x06,0x01 
rend_022: dl rend_022_0,rend_022_1,rend_022_2,rend_022_3
rend_022_0:
	ld hl,0x2501A3 ; BUF_14_37
	call render_panel
	ld hl,0x2F01A9 ; BUF_14_47
	call render_panel
	ld hl,0x3301AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_022_1:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_022_2:
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_022_3:
	jp render_scene_return
; 0x17 : 07,01 : 0x07,0x01 
rend_023: dl rend_023_0,rend_023_1,rend_023_2,rend_023_3
rend_023_0:
	ld hl,0x17019B ; BUF_14_23
	call render_panel
	ld hl,0x2501A3 ; BUF_14_37
	call render_panel
	ld hl,0x2B01A6 ; BUF_14_42
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_023_1:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_023_2:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_023_3:
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
; 0x18 : 08,01 : 0x08,0x01 
rend_024:
; 0x19 : 09,01 : 0x09,0x01 
rend_025: dl rend_025_0,rend_025_1,rend_025_2,rend_025_3
rend_025_0:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_025_1:
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x210113 ; BUF_10_30
	call render_panel
	ld hl,0x24020B ; BUF_17_36
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_025_2:
	ld hl,0x0B010A ; BUF_10_14
	call render_panel
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E0222 ; BUF_30_14
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x130200 ; BUF_17_19
	call render_panel
	jp render_scene_return
rend_025_3:
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
; 0x1A : 10,01 : 0x0A,0x01 
rend_026: dl rend_026_0,rend_026_1,rend_026_2,rend_026_3
rend_026_0:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_026_1:
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x200113 ; BUF_10_30
	call render_panel
	ld hl,0x210208 ; BUF_17_30
	call render_panel
	ld hl,0x23020A ; BUF_17_35
	call render_panel
	jp render_scene_return
rend_026_2:
	ld hl,0x1B0113 ; BUF_10_30
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E022B ; BUF_30_30
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	jp render_scene_return
rend_026_3:
	jp render_scene_return
; 0x1B : 11,01 : 0x0B,0x01 
rend_027: dl rend_027_0,rend_027_1,rend_027_2,rend_027_3
rend_027_0:
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	jp render_scene_return
rend_027_1:
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x220209 ; BUF_17_34
	call render_panel
	ld hl,0x270119 ; BUF_10_39
	call render_panel
	jp render_scene_return
rend_027_2:
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A0232 ; BUF_30_42
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	jp render_scene_return
rend_027_3:
	jp render_scene_return
; 0x1C : 12,01 : 0x0C,0x01 
rend_028: dl rend_028_0,rend_028_1,rend_028_2,rend_028_3
rend_028_0:
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x210208 ; BUF_17_30
	call render_panel
	jp render_scene_return
rend_028_1:
	ld hl,0x1B0208 ; BUF_17_30
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x260118 ; BUF_10_38
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
rend_028_2:
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320237 ; BUF_30_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	jp render_scene_return
rend_028_3:
	jp render_scene_return
; 0x1D : 13,01 : 0x0D,0x01 
rend_029: dl rend_029_0,rend_029_1,rend_029_2,rend_029_3
rend_029_0:
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x1101FF ; BUF_17_14
	call render_panel
	ld hl,0x1A0207 ; BUF_17_26
	call render_panel
	jp render_scene_return
rend_029_1:
	ld hl,0x1B0113 ; BUF_10_30
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_029_2:
	ld hl,0x36023A ; BUF_30_54
	call render_panel
	jp render_scene_return
rend_029_3:
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
; 0x1E : 14,01 : 0x0E,0x01 
rend_030:
; 0x1F : 15,01 : 0x0F,0x01 
rend_031: dl rend_031_0,rend_031_1,rend_031_2,rend_031_3
rend_031_0:
	ld hl,0x36023A ; BUF_30_54
	call render_panel
	jp render_scene_return
rend_031_1:
	ld hl,0x240116 ; BUF_10_36
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_031_2:
	jp render_scene_return
rend_031_3:
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
; 0x20 : 00,02 : 0x00,0x02 
rend_032: dl rend_032_0,rend_032_1,rend_032_2,rend_032_3
rend_032_0:
	jp render_scene_return
rend_032_1:
	jp render_scene_return
rend_032_2:
	ld hl,0x2A01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_032_3:
	jp render_scene_return
; 0x21 : 01,02 : 0x01,0x02 
rend_033: dl rend_033_0,rend_033_1,rend_033_2,rend_033_3
rend_033_0:
	jp render_scene_return
rend_033_1:
	jp render_scene_return
rend_033_2:
	ld hl,0x3201AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_033_3:
	jp render_scene_return
; 0x22 : 02,02 : 0x02,0x02 
rend_034: dl rend_034_0,rend_034_1,rend_034_2,rend_034_3
rend_034_0:
	jp render_scene_return
rend_034_1:
	jp render_scene_return
rend_034_2:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
rend_034_3:
	jp render_scene_return
; 0x23 : 03,02 : 0x03,0x02 
rend_035:
; 0x24 : 04,02 : 0x04,0x02 
rend_036:
; 0x25 : 05,02 : 0x05,0x02 
rend_037: dl rend_037_0,rend_037_1,rend_037_2,rend_037_3
rend_037_0:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
rend_037_1:
	jp render_scene_return
rend_037_2:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_037_3:
	jp render_scene_return
; 0x26 : 06,02 : 0x06,0x02 
rend_038:
; 0x27 : 07,02 : 0x07,0x02 
rend_039:
; 0x28 : 08,02 : 0x08,0x02 
rend_040:
; 0x29 : 09,02 : 0x09,0x02 
rend_041: dl rend_041_0,rend_041_1,rend_041_2,rend_041_3
rend_041_0:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_041_1:
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	jp render_scene_return
rend_041_2:
	ld hl,0x0C010A ; BUF_10_14
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F0222 ; BUF_30_14
	call render_panel
	ld hl,0x10010A ; BUF_10_14
	call render_panel
	ld hl,0x140201 ; BUF_17_20
	call render_panel
	ld hl,0x220114 ; BUF_10_34
	call render_panel
	jp render_scene_return
rend_041_3:
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
; 0x2A : 10,02 : 0x0A,0x02 
rend_042: dl rend_042_0,rend_042_1,rend_042_2,rend_042_3
rend_042_0:
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_042_1:
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x2C011A ; BUF_10_42
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_042_2:
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F022B ; BUF_30_30
	call render_panel
	ld hl,0x200113 ; BUF_10_30
	call render_panel
	ld hl,0x220209 ; BUF_17_34
	call render_panel
	jp render_scene_return
rend_042_3:
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
; 0x2B : 11,02 : 0x0B,0x02 
rend_043: dl rend_043_0,rend_043_1,rend_043_2,rend_043_3
rend_043_0:
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	jp render_scene_return
rend_043_1:
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	jp render_scene_return
rend_043_2:
	ld hl,0x28011A ; BUF_10_42
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B0232 ; BUF_30_42
	call render_panel
	ld hl,0x2C011A ; BUF_10_42
	call render_panel
	jp render_scene_return
rend_043_3:
	jp render_scene_return
; 0x2C : 12,02 : 0x0C,0x02 
rend_044: dl rend_044_0,rend_044_1,rend_044_2,rend_044_3
rend_044_0:
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x27020E ; BUF_17_39
	call render_panel
	jp render_scene_return
rend_044_1:
	ld hl,0x28011A ; BUF_10_42
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x30011E ; BUF_10_48
	call render_panel
	jp render_scene_return
rend_044_2:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330237 ; BUF_30_50
	call render_panel
	jp render_scene_return
rend_044_3:
	ld hl,0x2D011B ; BUF_10_45
	call render_panel
	jp render_scene_return
; 0x2D : 13,02 : 0x0D,0x02 
rend_045: dl rend_045_0,rend_045_1,rend_045_2,rend_045_3
rend_045_0:
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x190206 ; BUF_17_25
	call render_panel
	ld hl,0x270119 ; BUF_10_39
	call render_panel
	jp render_scene_return
rend_045_1:
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_045_2:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_045_3:
	ld hl,0x2E011C ; BUF_10_46
	call render_panel
	ld hl,0x340238 ; BUF_30_52
	call render_panel
	jp render_scene_return
; 0x2E : 14,02 : 0x0E,0x02 
rend_046:
; 0x2F : 15,02 : 0x0F,0x02 
rend_047: dl rend_047_0,rend_047_1,rend_047_2,rend_047_3
rend_047_0:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_047_1:
	ld hl,0x2E011C ; BUF_10_46
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_047_2:
	jp render_scene_return
rend_047_3:
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350239 ; BUF_30_53
	call render_panel
	jp render_scene_return
; 0x30 : 00,03 : 0x00,0x03 
rend_048: dl rend_048_0,rend_048_1,rend_048_2,rend_048_3
rend_048_0:
	jp render_scene_return
rend_048_1:
	jp render_scene_return
rend_048_2:
	ld hl,0x2901A6 ; BUF_14_42
	call render_panel
	ld hl,0x2B01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_048_3:
	jp render_scene_return
; 0x31 : 01,03 : 0x01,0x03 
rend_049: dl rend_049_0,rend_049_1,rend_049_2,rend_049_3
rend_049_0:
	jp render_scene_return
rend_049_1:
	jp render_scene_return
rend_049_2:
	jp render_scene_return
rend_049_3:
	jp render_scene_return
; 0x32 : 02,03 : 0x02,0x03 
rend_050:
; 0x33 : 03,03 : 0x03,0x03 
rend_051: dl rend_051_0,rend_051_1,rend_051_2,rend_051_3
rend_051_0:
	jp render_scene_return
rend_051_1:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
rend_051_2:
	ld hl,0x3401AC ; BUF_14_52
	call render_panel
	ld hl,0x3501AD ; BUF_14_53
	call render_panel
	jp render_scene_return
rend_051_3:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
; 0x34 : 04,03 : 0x04,0x03 
rend_052: dl rend_052_0,rend_052_1,rend_052_2,rend_052_3
rend_052_0:
	ld hl,0x3401AC ; BUF_14_52
	call render_panel
	ld hl,0x3501AD ; BUF_14_53
	call render_panel
	jp render_scene_return
rend_052_1:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
rend_052_2:
	jp render_scene_return
rend_052_3:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
; 0x35 : 05,03 : 0x05,0x03 
rend_053:
; 0x36 : 06,03 : 0x06,0x03 
rend_054: dl rend_054_0,rend_054_1,rend_054_2,rend_054_3
rend_054_0:
	jp render_scene_return
rend_054_1:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_054_2:
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_054_3:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
; 0x37 : 07,03 : 0x07,0x03 
rend_055: dl rend_055_0,rend_055_1,rend_055_2,rend_055_3
rend_055_0:
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_055_1:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_055_2:
	jp render_scene_return
rend_055_3:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
; 0x38 : 08,03 : 0x08,0x03 
rend_056:
; 0x39 : 09,03 : 0x09,0x03 
rend_057: dl rend_057_0,rend_057_1,rend_057_2,rend_057_3
rend_057_0:
	jp render_scene_return
rend_057_1:
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_057_2:
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x100222 ; BUF_30_14
	call render_panel
	ld hl,0x11010A ; BUF_10_14
	call render_panel
	ld hl,0x150202 ; BUF_17_21
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x230115 ; BUF_10_35
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_057_3:
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
; 0x3A : 10,03 : 0x0A,0x03 
rend_058: dl rend_058_0,rend_058_1,rend_058_2,rend_058_3
rend_058_0:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_058_1:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_058_2:
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	ld hl,0x20022B ; BUF_30_30
	call render_panel
	ld hl,0x210113 ; BUF_10_30
	call render_panel
	ld hl,0x23020A ; BUF_17_35
	call render_panel
	ld hl,0x2D011B ; BUF_10_45
	call render_panel
	jp render_scene_return
rend_058_3:
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x30011E ; BUF_10_48
	call render_panel
	jp render_scene_return
; 0x3B : 11,03 : 0x0B,0x03 
rend_059: dl rend_059_0,rend_059_1,rend_059_2,rend_059_3
rend_059_0:
	ld hl,0x28011A ; BUF_10_42
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
rend_059_1:
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	jp render_scene_return
rend_059_2:
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	ld hl,0x2C0232 ; BUF_30_42
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_059_3:
	ld hl,0x220114 ; BUF_10_34
	call render_panel
	ld hl,0x27020E ; BUF_17_39
	call render_panel
	jp render_scene_return
; 0x3C : 12,03 : 0x0C,0x03 
rend_060: dl rend_060_0,rend_060_1,rend_060_2,rend_060_3
rend_060_0:
	ld hl,0x1B0208 ; BUF_17_30
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x30011E ; BUF_10_48
	call render_panel
	jp render_scene_return
rend_060_1:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_060_2:
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	jp render_scene_return
rend_060_3:
	ld hl,0x230115 ; BUF_10_35
	call render_panel
	ld hl,0x2D0233 ; BUF_30_45
	call render_panel
	jp render_scene_return
; 0x3D : 13,03 : 0x0D,0x03 
rend_061: dl rend_061_0,rend_061_1,rend_061_2,rend_061_3
rend_061_0:
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x0C010A ; BUF_10_14
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x180205 ; BUF_17_24
	call render_panel
	ld hl,0x260118 ; BUF_10_38
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
rend_061_1:
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_061_2:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_061_3:
	ld hl,0x240116 ; BUF_10_36
	call render_panel
	ld hl,0x2E0234 ; BUF_30_46
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
; 0x3E : 14,03 : 0x0E,0x03 
rend_062:
; 0x3F : 15,03 : 0x0F,0x03 
rend_063: dl rend_063_0,rend_063_1,rend_063_2,rend_063_3
rend_063_0:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_063_1:
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_063_2:
	jp render_scene_return
rend_063_3:
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2F0235 ; BUF_30_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
; 0x40 : 00,04 : 0x00,0x04 
rend_064: dl rend_064_0,rend_064_1,rend_064_2,rend_064_3
rend_064_0:
	jp render_scene_return
rend_064_1:
	jp render_scene_return
rend_064_2:
	ld hl,0x2A01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_064_3:
	jp render_scene_return
; 0x41 : 01,04 : 0x01,0x04 
rend_065: dl rend_065_0,rend_065_1,rend_065_2,rend_065_3
rend_065_0:
	jp render_scene_return
rend_065_1:
	jp render_scene_return
rend_065_2:
	ld hl,0x3201AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_065_3:
	jp render_scene_return
; 0x42 : 02,04 : 0x02,0x04 
rend_066: dl rend_066_0,rend_066_1,rend_066_2,rend_066_3
rend_066_0:
	jp render_scene_return
rend_066_1:
	jp render_scene_return
rend_066_2:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
rend_066_3:
	jp render_scene_return
; 0x43 : 03,04 : 0x03,0x04 
rend_067:
; 0x44 : 04,04 : 0x04,0x04 
rend_068:
; 0x45 : 05,04 : 0x05,0x04 
rend_069: dl rend_069_0,rend_069_1,rend_069_2,rend_069_3
rend_069_0:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
rend_069_1:
	jp render_scene_return
rend_069_2:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_069_3:
	jp render_scene_return
; 0x46 : 06,04 : 0x06,0x04 
rend_070:
; 0x47 : 07,04 : 0x07,0x04 
rend_071:
; 0x48 : 08,04 : 0x08,0x04 
rend_072:
; 0x49 : 09,04 : 0x09,0x04 
rend_073: dl rend_073_0,rend_073_1,rend_073_2,rend_073_3
rend_073_0:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_073_1:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_073_2:
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x10010A ; BUF_10_14
	call render_panel
	ld hl,0x110222 ; BUF_30_14
	call render_panel
	ld hl,0x12010A ; BUF_10_14
	call render_panel
	ld hl,0x160203 ; BUF_17_22
	call render_panel
	ld hl,0x240116 ; BUF_10_36
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_073_3:
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	jp render_scene_return
; 0x4A : 10,04 : 0x0A,0x04 
rend_074: dl rend_074_0,rend_074_1,rend_074_2,rend_074_3
rend_074_0:
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_074_1:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_074_2:
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x200113 ; BUF_10_30
	call render_panel
	ld hl,0x21022B ; BUF_30_30
	call render_panel
	ld hl,0x24020B ; BUF_17_36
	call render_panel
	ld hl,0x2E011C ; BUF_10_46
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_074_3:
	ld hl,0x13010B ; BUF_10_19
	call render_panel
	ld hl,0x180205 ; BUF_17_24
	call render_panel
	ld hl,0x260118 ; BUF_10_38
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
; 0x4B : 11,04 : 0x0B,0x04 
rend_075: dl rend_075_0,rend_075_1,rend_075_2,rend_075_3
rend_075_0:
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_075_1:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_075_2:
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x2C011A ; BUF_10_42
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_075_3:
	ld hl,0x14010C ; BUF_10_20
	call render_panel
	ld hl,0x190206 ; BUF_17_25
	call render_panel
	ld hl,0x22022C ; BUF_30_34
	call render_panel
	ld hl,0x270119 ; BUF_10_39
	call render_panel
	jp render_scene_return
; 0x4C : 12,04 : 0x0C,0x04 
rend_076: dl rend_076_0,rend_076_1,rend_076_2,rend_076_3
rend_076_0:
	ld hl,0x1B0113 ; BUF_10_30
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_076_1:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_076_2:
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_076_3:
	ld hl,0x15010D ; BUF_10_21
	call render_panel
	ld hl,0x1A0207 ; BUF_17_26
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x23022D ; BUF_30_35
	call render_panel
	ld hl,0x2D011B ; BUF_10_45
	call render_panel
	jp render_scene_return
; 0x4D : 13,04 : 0x0D,0x04 
rend_077: dl rend_077_0,rend_077_1,rend_077_2,rend_077_3
rend_077_0:
	ld hl,0x0A01FF ; BUF_17_14
	call render_panel
	ld hl,0x0B010A ; BUF_10_14
	call render_panel
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_077_1:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_077_2:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_077_3:
	ld hl,0x16010E ; BUF_10_22
	call render_panel
	ld hl,0x24022E ; BUF_30_36
	call render_panel
	ld hl,0x2E011C ; BUF_10_46
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
; 0x4E : 14,04 : 0x0E,0x04 
rend_078:
; 0x4F : 15,04 : 0x0F,0x04 
rend_079: dl rend_079_0,rend_079_1,rend_079_2,rend_079_3
rend_079_0:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
rend_079_1:
	jp render_scene_return
rend_079_2:
	jp render_scene_return
rend_079_3:
	ld hl,0x17010F ; BUF_10_23
	call render_panel
	ld hl,0x25022F ; BUF_30_37
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
; 0x50 : 00,05 : 0x00,0x05 
rend_080: dl rend_080_0,rend_080_1,rend_080_2,rend_080_3
rend_080_0:
	jp render_scene_return
rend_080_1:
	jp render_scene_return
rend_080_2:
	ld hl,0x17019B ; BUF_14_23
	call render_panel
	ld hl,0x2501A3 ; BUF_14_37
	call render_panel
	ld hl,0x2B01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_080_3:
	jp render_scene_return
; 0x51 : 01,05 : 0x01,0x05 
rend_081: dl rend_081_0,rend_081_1,rend_081_2,rend_081_3
rend_081_0:
	jp render_scene_return
rend_081_1:
	jp render_scene_return
rend_081_2:
	ld hl,0x0501FA ; BUF_17_05
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x2501A3 ; BUF_14_37
	call render_panel
	ld hl,0x2F01A9 ; BUF_14_47
	call render_panel
	ld hl,0x3301AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_081_3:
	jp render_scene_return
; 0x52 : 02,05 : 0x02,0x05 
rend_082: dl rend_082_0,rend_082_1,rend_082_2,rend_082_3
rend_082_0:
	jp render_scene_return
rend_082_1:
	jp render_scene_return
rend_082_2:
	ld hl,0x050105 ; BUF_10_05
	call render_panel
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x2F01A9 ; BUF_14_47
	call render_panel
	ld hl,0x3501AD ; BUF_14_53
	call render_panel
	jp render_scene_return
rend_082_3:
	ld hl,0x3401AC ; BUF_14_52
	call render_panel
	jp render_scene_return
; 0x53 : 03,05 : 0x03,0x05 
rend_083: dl rend_083_0,rend_083_1,rend_083_2,rend_083_3
rend_083_0:
	jp render_scene_return
rend_083_1:
	jp render_scene_return
rend_083_2:
	ld hl,0x0501FA ; BUF_17_05
	call render_panel
	ld hl,0x17010F ; BUF_10_23
	call render_panel
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x3501AD ; BUF_14_53
	call render_panel
	jp render_scene_return
rend_083_3:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
; 0x54 : 04,05 : 0x04,0x05 
rend_084: dl rend_084_0,rend_084_1,rend_084_2,rend_084_3
rend_084_0:
	ld hl,0x3401AC ; BUF_14_52
	call render_panel
	jp render_scene_return
rend_084_1:
	jp render_scene_return
rend_084_2:
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_084_3:
	ld hl,0x3601AE ; BUF_14_54
	call render_panel
	jp render_scene_return
; 0x55 : 05,05 : 0x05,0x05 
rend_085: dl rend_085_0,rend_085_1,rend_085_2,rend_085_3
rend_085_0:
	ld hl,0x2E01A8 ; BUF_14_46
	call render_panel
	ld hl,0x3401AC ; BUF_14_52
	call render_panel
	jp render_scene_return
rend_085_1:
	jp render_scene_return
rend_085_2:
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_085_3:
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	ld hl,0x3501AD ; BUF_14_53
	call render_panel
	jp render_scene_return
; 0x56 : 06,05 : 0x06,0x05 
rend_086: dl rend_086_0,rend_086_1,rend_086_2,rend_086_3
rend_086_0:
	ld hl,0x2401A2 ; BUF_14_36
	call render_panel
	ld hl,0x2E01A8 ; BUF_14_46
	call render_panel
	ld hl,0x3101AB ; BUF_14_50
	call render_panel
	jp render_scene_return
rend_086_1:
	jp render_scene_return
rend_086_2:
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_086_3:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
; 0x57 : 07,05 : 0x07,0x05 
rend_087: dl rend_087_0,rend_087_1,rend_087_2,rend_087_3
rend_087_0:
	ld hl,0x16019A ; BUF_14_22
	call render_panel
	ld hl,0x2401A2 ; BUF_14_36
	call render_panel
	ld hl,0x2901A6 ; BUF_14_42
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_087_1:
	jp render_scene_return
rend_087_2:
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_087_3:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
; 0x58 : 08,05 : 0x08,0x05 
rend_088: dl rend_088_0,rend_088_1,rend_088_2,rend_088_3
rend_088_0:
	ld hl,0x040190 ; BUF_14_04
	call render_panel
	ld hl,0x0D0196 ; BUF_14_14
	call render_panel
	ld hl,0x16019A ; BUF_14_22
	call render_panel
	ld hl,0x1D019F ; BUF_14_30
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_088_1:
	jp render_scene_return
rend_088_2:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_088_3:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
; 0x59 : 09,05 : 0x09,0x05 
rend_089:
; 0x5A : 10,05 : 0x0A,0x05 
rend_090:
; 0x5B : 11,05 : 0x0B,0x05 
rend_091:
; 0x5C : 12,05 : 0x0C,0x05 
rend_092:
; 0x5D : 13,05 : 0x0D,0x05 
rend_093:
; 0x5E : 14,05 : 0x0E,0x05 
rend_094: dl rend_094_0,rend_094_1,rend_094_2,rend_094_3
rend_094_0:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
rend_094_1:
	jp render_scene_return
rend_094_2:
	jp render_scene_return
rend_094_3:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
; 0x5F : 15,05 : 0x0F,0x05 
rend_095: dl rend_095_0,rend_095_1,rend_095_2,rend_095_3
rend_095_0:
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_095_1:
	jp render_scene_return
rend_095_2:
	jp render_scene_return
rend_095_3:
	ld hl,0x050105 ; BUF_10_05
	call render_panel
	ld hl,0x170227 ; BUF_30_23
	call render_panel
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
; 0x60 : 00,06 : 0x00,0x06 
rend_096: dl rend_096_0,rend_096_1,rend_096_2,rend_096_3
rend_096_0:
	jp render_scene_return
rend_096_1:
	jp render_scene_return
rend_096_2:
	ld hl,0x18019C ; BUF_14_24
	call render_panel
	ld hl,0x2601A4 ; BUF_14_38
	call render_panel
	ld hl,0x2C01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_096_3:
	jp render_scene_return
; 0x61 : 01,06 : 0x01,0x06 
rend_097: dl rend_097_0,rend_097_1,rend_097_2,rend_097_3
rend_097_0:
	jp render_scene_return
rend_097_1:
	jp render_scene_return
rend_097_2:
	ld hl,0x0601FB ; BUF_17_06
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x2601A4 ; BUF_14_38
	call render_panel
	ld hl,0x3001AA ; BUF_14_48
	call render_panel
	jp render_scene_return
rend_097_3:
	ld hl,0x2D01A7 ; BUF_14_45
	call render_panel
	jp render_scene_return
; 0x62 : 02,06 : 0x02,0x06 
rend_098: dl rend_098_0,rend_098_1,rend_098_2,rend_098_3
rend_098_0:
	jp render_scene_return
rend_098_1:
	jp render_scene_return
rend_098_2:
	ld hl,0x060106 ; BUF_10_06
	call render_panel
	ld hl,0x180205 ; BUF_17_24
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x3001AA ; BUF_14_48
	call render_panel
	jp render_scene_return
rend_098_3:
	ld hl,0x2E01A8 ; BUF_14_46
	call render_panel
	ld hl,0x3101AB ; BUF_14_50
	call render_panel
	jp render_scene_return
; 0x63 : 03,06 : 0x03,0x06 
rend_099: dl rend_099_0,rend_099_1,rend_099_2,rend_099_3
rend_099_0:
	jp render_scene_return
rend_099_1:
	jp render_scene_return
rend_099_2:
	ld hl,0x0601FB ; BUF_17_06
	call render_panel
	ld hl,0x180110 ; BUF_10_24
	call render_panel
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	jp render_scene_return
rend_099_3:
	ld hl,0x3101AB ; BUF_14_50
	call render_panel
	ld hl,0x3201AB ; BUF_14_50
	call render_panel
	jp render_scene_return
; 0x64 : 04,06 : 0x04,0x06 
rend_100: dl rend_100_0,rend_100_1,rend_100_2,rend_100_3
rend_100_0:
	jp render_scene_return
rend_100_1:
	jp render_scene_return
rend_100_2:
	ld hl,0x0501FA ; BUF_17_05
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x180205 ; BUF_17_24
	call render_panel
	ld hl,0x260118 ; BUF_10_38
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
rend_100_3:
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	ld hl,0x3201AB ; BUF_14_50
	call render_panel
	ld hl,0x3301AB ; BUF_14_50
	call render_panel
	jp render_scene_return
; 0x65 : 05,06 : 0x05,0x06 
rend_101: dl rend_101_0,rend_101_1,rend_101_2,rend_101_3
rend_101_0:
	ld hl,0x2D01A7 ; BUF_14_45
	call render_panel
	jp render_scene_return
rend_101_1:
	jp render_scene_return
rend_101_2:
	ld hl,0x050105 ; BUF_10_05
	call render_panel
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x30011E ; BUF_10_48
	call render_panel
	jp render_scene_return
rend_101_3:
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x2F01A9 ; BUF_14_47
	call render_panel
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x3301AB ; BUF_14_50
	call render_panel
	jp render_scene_return
; 0x66 : 06,06 : 0x06,0x06 
rend_102: dl rend_102_0,rend_102_1,rend_102_2,rend_102_3
rend_102_0:
	ld hl,0x2301A1 ; BUF_14_35
	call render_panel
	ld hl,0x2D01A7 ; BUF_14_45
	call render_panel
	jp render_scene_return
rend_102_1:
	jp render_scene_return
rend_102_2:
	ld hl,0x0501FA ; BUF_17_05
	call render_panel
	ld hl,0x17010F ; BUF_10_23
	call render_panel
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
rend_102_3:
	ld hl,0x3001AA ; BUF_14_48
	call render_panel
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	jp render_scene_return
; 0x67 : 07,06 : 0x07,0x06 
rend_103: dl rend_103_0,rend_103_1,rend_103_2,rend_103_3
rend_103_0:
	ld hl,0x150199 ; BUF_14_21
	call render_panel
	ld hl,0x1C019F ; BUF_14_30
	call render_panel
	ld hl,0x2301A1 ; BUF_14_35
	call render_panel
	ld hl,0x2801A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
rend_103_1:
	jp render_scene_return
rend_103_2:
	ld hl,0x050105 ; BUF_10_05
	call render_panel
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_103_3:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
; 0x68 : 08,06 : 0x08,0x06 
rend_104: dl rend_104_0,rend_104_1,rend_104_2,rend_104_3
rend_104_0:
	ld hl,0x03018F ; BUF_14_03
	call render_panel
	ld hl,0x150199 ; BUF_14_21
	call render_panel
	ld hl,0x1C019F ; BUF_14_30
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_104_1:
	jp render_scene_return
rend_104_2:
	ld hl,0x0501FA ; BUF_17_05
	call render_panel
	ld hl,0x17010F ; BUF_10_23
	call render_panel
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_104_3:
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
; 0x69 : 09,06 : 0x09,0x06 
rend_105: dl rend_105_0,rend_105_1,rend_105_2,rend_105_3
rend_105_0:
	ld hl,0x03018F ; BUF_14_03
	call render_panel
	ld hl,0x0C0196 ; BUF_14_14
	call render_panel
	ld hl,0x23020A ; BUF_17_35
	call render_panel
	ld hl,0x2D011B ; BUF_10_45
	call render_panel
	jp render_scene_return
rend_105_1:
	jp render_scene_return
rend_105_2:
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_105_3:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
; 0x6A : 10,06 : 0x0A,0x06 
rend_106: dl rend_106_0,rend_106_1,rend_106_2,rend_106_3
rend_106_0:
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_106_1:
	jp render_scene_return
rend_106_2:
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_106_3:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
; 0x6B : 11,06 : 0x0B,0x06 
rend_107: dl rend_107_0,rend_107_1,rend_107_2,rend_107_3
rend_107_0:
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_107_1:
	jp render_scene_return
rend_107_2:
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x350121 ; BUF_10_53
	call render_panel
	jp render_scene_return
rend_107_3:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
; 0x6C : 12,06 : 0x0C,0x06 
rend_108: dl rend_108_0,rend_108_1,rend_108_2,rend_108_3
rend_108_0:
	ld hl,0x24020B ; BUF_17_36
	call render_panel
	ld hl,0x2E011C ; BUF_10_46
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_108_1:
	jp render_scene_return
rend_108_2:
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
rend_108_3:
	ld hl,0x360122 ; BUF_10_54
	call render_panel
	jp render_scene_return
; 0x6D : 13,06 : 0x0D,0x06 
rend_109: dl rend_109_0,rend_109_1,rend_109_2,rend_109_3
rend_109_0:
	ld hl,0x160203 ; BUF_17_22
	call render_panel
	ld hl,0x240116 ; BUF_10_36
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x340120 ; BUF_10_52
	call render_panel
	jp render_scene_return
rend_109_1:
	jp render_scene_return
rend_109_2:
	jp render_scene_return
rend_109_3:
	ld hl,0x360217 ; BUF_17_54
	call render_panel
	jp render_scene_return
; 0x6E : 14,06 : 0x0E,0x06 
rend_110: dl rend_110_0,rend_110_1,rend_110_2,rend_110_3
rend_110_0:
	ld hl,0x0401F9 ; BUF_17_04
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x16010E ; BUF_10_22
	call render_panel
	ld hl,0x24020B ; BUF_17_36
	call render_panel
	ld hl,0x2E011C ; BUF_10_46
	call render_panel
	ld hl,0x340215 ; BUF_17_52
	call render_panel
	jp render_scene_return
rend_110_1:
	jp render_scene_return
rend_110_2:
	jp render_scene_return
rend_110_3:
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x350216 ; BUF_17_53
	call render_panel
	jp render_scene_return
; 0x6F : 15,06 : 0x0F,0x06 
rend_111: dl rend_111_0,rend_111_1,rend_111_2,rend_111_3
rend_111_0:
	ld hl,0x040104 ; BUF_10_04
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x160203 ; BUF_17_22
	call render_panel
	ld hl,0x240116 ; BUF_10_36
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	jp render_scene_return
rend_111_1:
	jp render_scene_return
rend_111_2:
	jp render_scene_return
rend_111_3:
	ld hl,0x05021D ; BUF_30_05
	call render_panel
	ld hl,0x17010F ; BUF_10_23
	call render_panel
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2F011D ; BUF_10_47
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	jp render_scene_return
; 0x70 : 00,07 : 0x00,0x07 
rend_112: dl rend_112_0,rend_112_1,rend_112_2,rend_112_3
rend_112_0:
	jp render_scene_return
rend_112_1:
	jp render_scene_return
rend_112_2:
	ld hl,0x19019D ; BUF_14_25
	call render_panel
	ld hl,0x2701A5 ; BUF_14_39
	call render_panel
	jp render_scene_return
rend_112_3:
	ld hl,0x2201A0 ; BUF_14_34
	call render_panel
	jp render_scene_return
; 0x71 : 01,07 : 0x01,0x07 
rend_113: dl rend_113_0,rend_113_1,rend_113_2,rend_113_3
rend_113_0:
	jp render_scene_return
rend_113_1:
	jp render_scene_return
rend_113_2:
	ld hl,0x0701FC ; BUF_17_07
	call render_panel
	ld hl,0x1101FF ; BUF_17_14
	call render_panel
	ld hl,0x2701A5 ; BUF_14_39
	call render_panel
	jp render_scene_return
rend_113_3:
	ld hl,0x2301A1 ; BUF_14_35
	call render_panel
	ld hl,0x2801A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
; 0x72 : 02,07 : 0x02,0x07 
rend_114: dl rend_114_0,rend_114_1,rend_114_2,rend_114_3
rend_114_0:
	jp render_scene_return
rend_114_1:
	jp render_scene_return
rend_114_2:
	ld hl,0x070107 ; BUF_10_07
	call render_panel
	ld hl,0x190206 ; BUF_17_25
	call render_panel
	ld hl,0x210208 ; BUF_17_30
	call render_panel
	jp render_scene_return
rend_114_3:
	ld hl,0x2401A2 ; BUF_14_36
	call render_panel
	ld hl,0x2801A6 ; BUF_14_42
	call render_panel
	ld hl,0x2901A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
; 0x73 : 03,07 : 0x03,0x07 
rend_115: dl rend_115_0,rend_115_1,rend_115_2,rend_115_3
rend_115_0:
	jp render_scene_return
rend_115_1:
	jp render_scene_return
rend_115_2:
	ld hl,0x0701FC ; BUF_17_07
	call render_panel
	ld hl,0x190111 ; BUF_10_25
	call render_panel
	ld hl,0x27020E ; BUF_17_39
	call render_panel
	jp render_scene_return
rend_115_3:
	ld hl,0x220209 ; BUF_17_34
	call render_panel
	ld hl,0x2901A6 ; BUF_14_42
	call render_panel
	ld hl,0x2A01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
; 0x74 : 04,07 : 0x04,0x07 
rend_116: dl rend_116_0,rend_116_1,rend_116_2,rend_116_3
rend_116_0:
	jp render_scene_return
rend_116_1:
	jp render_scene_return
rend_116_2:
	ld hl,0x0601FB ; BUF_17_06
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x190206 ; BUF_17_25
	call render_panel
	ld hl,0x270119 ; BUF_10_39
	call render_panel
	jp render_scene_return
rend_116_3:
	ld hl,0x23020A ; BUF_17_35
	call render_panel
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x2A01A6 ; BUF_14_42
	call render_panel
	ld hl,0x2B01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
; 0x75 : 05,07 : 0x05,0x07 
rend_117: dl rend_117_0,rend_117_1,rend_117_2,rend_117_3
rend_117_0:
	jp render_scene_return
rend_117_1:
	jp render_scene_return
rend_117_2:
	ld hl,0x060106 ; BUF_10_06
	call render_panel
	ld hl,0x180205 ; BUF_17_24
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x27020E ; BUF_17_39
	call render_panel
	jp render_scene_return
rend_117_3:
	ld hl,0x24020B ; BUF_17_36
	call render_panel
	ld hl,0x2501A3 ; BUF_14_37
	call render_panel
	ld hl,0x28011A ; BUF_10_42
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2B01A6 ; BUF_14_42
	call render_panel
	ld hl,0x2C01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
; 0x76 : 06,07 : 0x06,0x07 
rend_118: dl rend_118_0,rend_118_1,rend_118_2,rend_118_3
rend_118_0:
	ld hl,0x2201A0 ; BUF_14_34
	call render_panel
	jp render_scene_return
rend_118_1:
	jp render_scene_return
rend_118_2:
	ld hl,0x0601FB ; BUF_17_06
	call render_panel
	ld hl,0x180110 ; BUF_10_24
	call render_panel
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	jp render_scene_return
rend_118_3:
	ld hl,0x2601A4 ; BUF_14_38
	call render_panel
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2C01A6 ; BUF_14_42
	call render_panel
	jp render_scene_return
; 0x77 : 07,07 : 0x07,0x07 
rend_119: dl rend_119_0,rend_119_1,rend_119_2,rend_119_3
rend_119_0:
	ld hl,0x140198 ; BUF_14_20
	call render_panel
	ld hl,0x2201A0 ; BUF_14_34
	call render_panel
	jp render_scene_return
rend_119_1:
	jp render_scene_return
rend_119_2:
	ld hl,0x060106 ; BUF_10_06
	call render_panel
	ld hl,0x180205 ; BUF_17_24
	call render_panel
	ld hl,0x260118 ; BUF_10_38
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
rend_119_3:
	ld hl,0x2701A5 ; BUF_14_39
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
; 0x78 : 08,07 : 0x08,0x07 
rend_120: dl rend_120_0,rend_120_1,rend_120_2,rend_120_3
rend_120_0:
	ld hl,0x02018E ; BUF_14_02
	call render_panel
	ld hl,0x0B0196 ; BUF_14_14
	call render_panel
	ld hl,0x140198 ; BUF_14_20
	call render_panel
	ld hl,0x1B019F ; BUF_14_30
	call render_panel
	jp render_scene_return
rend_120_1:
	jp render_scene_return
rend_120_2:
	ld hl,0x0601FB ; BUF_17_06
	call render_panel
	ld hl,0x180110 ; BUF_10_24
	call render_panel
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x30011E ; BUF_10_48
	call render_panel
	jp render_scene_return
rend_120_3:
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	ld hl,0x2E0211 ; BUF_17_46
	call render_panel
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	jp render_scene_return
; 0x79 : 09,07 : 0x09,0x07 
rend_121: dl rend_121_0,rend_121_1,rend_121_2,rend_121_3
rend_121_0:
	ld hl,0x02018E ; BUF_14_02
	call render_panel
	ld hl,0x0B0196 ; BUF_14_14
	call render_panel
	ld hl,0x220209 ; BUF_17_34
	call render_panel
	jp render_scene_return
rend_121_1:
	jp render_scene_return
rend_121_2:
	ld hl,0x180205 ; BUF_17_24
	call render_panel
	ld hl,0x260118 ; BUF_10_38
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
rend_121_3:
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x2C011A ; BUF_10_42
	call render_panel
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	jp render_scene_return
; 0x7A : 10,07 : 0x0A,0x07 
rend_122: dl rend_122_0,rend_122_1,rend_122_2,rend_122_3
rend_122_0:
	ld hl,0x140201 ; BUF_17_20
	call render_panel
	ld hl,0x220114 ; BUF_10_34
	call render_panel
	jp render_scene_return
rend_122_1:
	jp render_scene_return
rend_122_2:
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x30011E ; BUF_10_48
	call render_panel
	jp render_scene_return
rend_122_3:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
; 0x7B : 11,07 : 0x0B,0x07 
rend_123: dl rend_123_0,rend_123_1,rend_123_2,rend_123_3
rend_123_0:
	ld hl,0x0201F7 ; BUF_17_02
	call render_panel
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x14010C ; BUF_10_20
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_123_1:
	jp render_scene_return
rend_123_2:
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
rend_123_3:
	ld hl,0x31011F ; BUF_10_50
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	jp render_scene_return
; 0x7C : 12,07 : 0x0C,0x07 
rend_124: dl rend_124_0,rend_124_1,rend_124_2,rend_124_3
rend_124_0:
	ld hl,0x23020A ; BUF_17_35
	call render_panel
	ld hl,0x2D011B ; BUF_10_45
	call render_panel
	jp render_scene_return
rend_124_1:
	jp render_scene_return
rend_124_2:
	jp render_scene_return
rend_124_3:
	ld hl,0x310214 ; BUF_17_50
	call render_panel
	ld hl,0x32011F ; BUF_10_50
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
; 0x7D : 13,07 : 0x0D,0x07 
rend_125: dl rend_125_0,rend_125_1,rend_125_2,rend_125_3
rend_125_0:
	ld hl,0x150202 ; BUF_17_21
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x230115 ; BUF_10_35
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_125_1:
	jp render_scene_return
rend_125_2:
	jp render_scene_return
rend_125_3:
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x320214 ; BUF_17_50
	call render_panel
	ld hl,0x33011F ; BUF_10_50
	call render_panel
	jp render_scene_return
; 0x7E : 14,07 : 0x0E,0x07 
rend_126: dl rend_126_0,rend_126_1,rend_126_2,rend_126_3
rend_126_0:
	ld hl,0x0301F8 ; BUF_17_03
	call render_panel
	ld hl,0x15010D ; BUF_10_21
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x23020A ; BUF_17_35
	call render_panel
	ld hl,0x2D011B ; BUF_10_45
	call render_panel
	jp render_scene_return
rend_126_1:
	jp render_scene_return
rend_126_2:
	jp render_scene_return
rend_126_3:
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2F0212 ; BUF_17_47
	call render_panel
	ld hl,0x330214 ; BUF_17_50
	call render_panel
	jp render_scene_return
; 0x7F : 15,07 : 0x0F,0x07 
rend_127: dl rend_127_0,rend_127_1,rend_127_2,rend_127_3
rend_127_0:
	ld hl,0x030103 ; BUF_10_03
	call render_panel
	ld hl,0x150202 ; BUF_17_21
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x230115 ; BUF_10_35
	call render_panel
	ld hl,0x2D0210 ; BUF_17_45
	call render_panel
	jp render_scene_return
rend_127_1:
	jp render_scene_return
rend_127_2:
	jp render_scene_return
rend_127_3:
	ld hl,0x050105 ; BUF_10_05
	call render_panel
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x250117 ; BUF_10_37
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	ld hl,0x300213 ; BUF_17_48
	call render_panel
	jp render_scene_return
; 0x80 : 00,08 : 0x00,0x08 
rend_128: dl rend_128_0,rend_128_1,rend_128_2,rend_128_3
rend_128_0:
	jp render_scene_return
rend_128_1:
	jp render_scene_return
rend_128_2:
	ld hl,0x1A019E ; BUF_14_26
	call render_panel
	jp render_scene_return
rend_128_3:
	ld hl,0x140198 ; BUF_14_20
	call render_panel
	ld hl,0x1B019F ; BUF_14_30
	call render_panel
	jp render_scene_return
; 0x81 : 01,08 : 0x01,0x08 
rend_129: dl rend_129_0,rend_129_1,rend_129_2,rend_129_3
rend_129_0:
	jp render_scene_return
rend_129_1:
	jp render_scene_return
rend_129_2:
	ld hl,0x0801FD ; BUF_17_08
	call render_panel
	ld hl,0x1201FF ; BUF_17_14
	call render_panel
	jp render_scene_return
rend_129_3:
	ld hl,0x150199 ; BUF_14_21
	call render_panel
	ld hl,0x1B019F ; BUF_14_30
	call render_panel
	ld hl,0x1C019F ; BUF_14_30
	call render_panel
	jp render_scene_return
; 0x82 : 02,08 : 0x02,0x08 
rend_130: dl rend_130_0,rend_130_1,rend_130_2,rend_130_3
rend_130_0:
	jp render_scene_return
rend_130_1:
	jp render_scene_return
rend_130_2:
	ld hl,0x080108 ; BUF_10_08
	call render_panel
	ld hl,0x1A0207 ; BUF_17_26
	call render_panel
	jp render_scene_return
rend_130_3:
	ld hl,0x130200 ; BUF_17_19
	call render_panel
	ld hl,0x16019A ; BUF_14_22
	call render_panel
	ld hl,0x1C019F ; BUF_14_30
	call render_panel
	ld hl,0x1D019F ; BUF_14_30
	call render_panel
	jp render_scene_return
; 0x83 : 03,08 : 0x03,0x08 
rend_131: dl rend_131_0,rend_131_1,rend_131_2,rend_131_3
rend_131_0:
	jp render_scene_return
rend_131_1:
	jp render_scene_return
rend_131_2:
	ld hl,0x0801FD ; BUF_17_08
	call render_panel
	ld hl,0x1A0112 ; BUF_10_26
	call render_panel
	jp render_scene_return
rend_131_3:
	ld hl,0x140201 ; BUF_17_20
	call render_panel
	ld hl,0x1B0208 ; BUF_17_30
	call render_panel
	ld hl,0x1D019F ; BUF_14_30
	call render_panel
	ld hl,0x1E019F ; BUF_14_30
	call render_panel
	jp render_scene_return
; 0x84 : 04,08 : 0x04,0x08 
rend_132: dl rend_132_0,rend_132_1,rend_132_2,rend_132_3
rend_132_0:
	jp render_scene_return
rend_132_1:
	jp render_scene_return
rend_132_2:
	ld hl,0x0701FC ; BUF_17_07
	call render_panel
	ld hl,0x1101FF ; BUF_17_14
	call render_panel
	ld hl,0x1A0207 ; BUF_17_26
	call render_panel
	jp render_scene_return
rend_132_3:
	ld hl,0x150202 ; BUF_17_21
	call render_panel
	ld hl,0x1B0113 ; BUF_10_30
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E019F ; BUF_14_30
	call render_panel
	ld hl,0x1F019F ; BUF_14_30
	call render_panel
	jp render_scene_return
; 0x85 : 05,08 : 0x05,0x08 
rend_133: dl rend_133_0,rend_133_1,rend_133_2,rend_133_3
rend_133_0:
	jp render_scene_return
rend_133_1:
	jp render_scene_return
rend_133_2:
	ld hl,0x070107 ; BUF_10_07
	call render_panel
	ld hl,0x190206 ; BUF_17_25
	call render_panel
	ld hl,0x210208 ; BUF_17_30
	call render_panel
	jp render_scene_return
rend_133_3:
	ld hl,0x160203 ; BUF_17_22
	call render_panel
	ld hl,0x17019B ; BUF_14_23
	call render_panel
	ld hl,0x1B0208 ; BUF_17_30
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F019F ; BUF_14_30
	call render_panel
	ld hl,0x20019F ; BUF_14_30
	call render_panel
	jp render_scene_return
; 0x86 : 06,08 : 0x06,0x08 
rend_134: dl rend_134_0,rend_134_1,rend_134_2,rend_134_3
rend_134_0:
	jp render_scene_return
rend_134_1:
	jp render_scene_return
rend_134_2:
	ld hl,0x0701FC ; BUF_17_07
	call render_panel
	ld hl,0x190111 ; BUF_10_25
	call render_panel
	ld hl,0x27020E ; BUF_17_39
	call render_panel
	jp render_scene_return
rend_134_3:
	ld hl,0x18019C ; BUF_14_24
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x20019F ; BUF_14_30
	call render_panel
	ld hl,0x21019F ; BUF_14_30
	call render_panel
	ld hl,0x220209 ; BUF_17_34
	call render_panel
	jp render_scene_return
; 0x87 : 07,08 : 0x07,0x08 
rend_135: dl rend_135_0,rend_135_1,rend_135_2,rend_135_3
rend_135_0:
	ld hl,0x130197 ; BUF_14_19
	call render_panel
	jp render_scene_return
rend_135_1:
	jp render_scene_return
rend_135_2:
	ld hl,0x070107 ; BUF_10_07
	call render_panel
	ld hl,0x190206 ; BUF_17_25
	call render_panel
	ld hl,0x270119 ; BUF_10_39
	call render_panel
	jp render_scene_return
rend_135_3:
	ld hl,0x19019D ; BUF_14_25
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x21019F ; BUF_14_30
	call render_panel
	ld hl,0x23020A ; BUF_17_35
	call render_panel
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	jp render_scene_return
; 0x88 : 08,08 : 0x08,0x08 
rend_136: dl rend_136_0,rend_136_1,rend_136_2,rend_136_3
rend_136_0:
	ld hl,0x01018D ; BUF_14_01
	call render_panel
	ld hl,0x130197 ; BUF_14_19
	call render_panel
	jp render_scene_return
rend_136_1:
	jp render_scene_return
rend_136_2:
	ld hl,0x0701FC ; BUF_17_07
	call render_panel
	ld hl,0x190111 ; BUF_10_25
	call render_panel
	ld hl,0x27020E ; BUF_17_39
	call render_panel
	jp render_scene_return
rend_136_3:
	ld hl,0x1A019E ; BUF_14_26
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x24020B ; BUF_17_36
	call render_panel
	ld hl,0x28011A ; BUF_10_42
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	jp render_scene_return
; 0x89 : 09,08 : 0x09,0x08 
rend_137: dl rend_137_0,rend_137_1,rend_137_2,rend_137_3
rend_137_0:
	ld hl,0x01018D ; BUF_14_01
	call render_panel
	ld hl,0x0A0196 ; BUF_14_14
	call render_panel
	jp render_scene_return
rend_137_1:
	jp render_scene_return
rend_137_2:
	ld hl,0x190206 ; BUF_17_25
	call render_panel
	ld hl,0x270119 ; BUF_10_39
	call render_panel
	jp render_scene_return
rend_137_3:
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x200113 ; BUF_10_30
	call render_panel
	ld hl,0x210208 ; BUF_17_30
	call render_panel
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	jp render_scene_return
; 0x8A : 10,08 : 0x0A,0x08 
rend_138: dl rend_138_0,rend_138_1,rend_138_2,rend_138_3
rend_138_0:
	ld hl,0x130200 ; BUF_17_19
	call render_panel
	jp render_scene_return
rend_138_1:
	jp render_scene_return
rend_138_2:
	ld hl,0x27020E ; BUF_17_39
	call render_panel
	jp render_scene_return
rend_138_3:
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x210113 ; BUF_10_30
	call render_panel
	ld hl,0x28011A ; BUF_10_42
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	jp render_scene_return
; 0x8B : 11,08 : 0x0B,0x08 
rend_139: dl rend_139_0,rend_139_1,rend_139_2,rend_139_3
rend_139_0:
	ld hl,0x0101F6 ; BUF_17_01
	call render_panel
	ld hl,0x13010B ; BUF_10_19
	call render_panel
	jp render_scene_return
rend_139_1:
	jp render_scene_return
rend_139_2:
	jp render_scene_return
rend_139_3:
	ld hl,0x28020F ; BUF_17_42
	call render_panel
	ld hl,0x29011A ; BUF_10_42
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	jp render_scene_return
; 0x8C : 12,08 : 0x0C,0x08 
rend_140: dl rend_140_0,rend_140_1,rend_140_2,rend_140_3
rend_140_0:
	ld hl,0x010101 ; BUF_10_01
	call render_panel
	ld hl,0x220209 ; BUF_17_34
	call render_panel
	jp render_scene_return
rend_140_1:
	jp render_scene_return
rend_140_2:
	jp render_scene_return
rend_140_3:
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x29020F ; BUF_17_42
	call render_panel
	ld hl,0x2A011A ; BUF_10_42
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x2C011A ; BUF_10_42
	call render_panel
	jp render_scene_return
; 0x8D : 13,08 : 0x0D,0x08 
rend_141: dl rend_141_0,rend_141_1,rend_141_2,rend_141_3
rend_141_0:
	ld hl,0x140201 ; BUF_17_20
	call render_panel
	ld hl,0x220114 ; BUF_10_34
	call render_panel
	jp render_scene_return
rend_141_1:
	jp render_scene_return
rend_141_2:
	jp render_scene_return
rend_141_3:
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x2A020F ; BUF_17_42
	call render_panel
	ld hl,0x2B011A ; BUF_10_42
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	jp render_scene_return
; 0x8E : 14,08 : 0x0E,0x08 
rend_142: dl rend_142_0,rend_142_1,rend_142_2,rend_142_3
rend_142_0:
	ld hl,0x0201F7 ; BUF_17_02
	call render_panel
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x14010C ; BUF_10_20
	call render_panel
	ld hl,0x220209 ; BUF_17_34
	call render_panel
	jp render_scene_return
rend_142_1:
	jp render_scene_return
rend_142_2:
	jp render_scene_return
rend_142_3:
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x25020C ; BUF_17_37
	call render_panel
	ld hl,0x2B020F ; BUF_17_42
	call render_panel
	ld hl,0x2C011A ; BUF_10_42
	call render_panel
	jp render_scene_return
; 0x8F : 15,08 : 0x0F,0x08 
rend_143: dl rend_143_0,rend_143_1,rend_143_2,rend_143_3
rend_143_0:
	ld hl,0x020102 ; BUF_10_02
	call render_panel
	ld hl,0x0B010A ; BUF_10_14
	call render_panel
	ld hl,0x140201 ; BUF_17_20
	call render_panel
	ld hl,0x220114 ; BUF_10_34
	call render_panel
	jp render_scene_return
rend_143_1:
	jp render_scene_return
rend_143_2:
	jp render_scene_return
rend_143_3:
	ld hl,0x0501FA ; BUF_17_05
	call render_panel
	ld hl,0x17010F ; BUF_10_23
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	ld hl,0x26020D ; BUF_17_38
	call render_panel
	ld hl,0x2C020F ; BUF_17_42
	call render_panel
	jp render_scene_return
; 0x90 : 00,09 : 0x00,0x09 
rend_144: dl rend_144_0,rend_144_1,rend_144_2,rend_144_3
rend_144_0:
	jp render_scene_return
rend_144_1:
	jp render_scene_return
rend_144_2:
	jp render_scene_return
rend_144_3:
	ld hl,0x02018E ; BUF_14_02
	call render_panel
	ld hl,0x0A0196 ; BUF_14_14
	call render_panel
	ld hl,0x0B0196 ; BUF_14_14
	call render_panel
	jp render_scene_return
; 0x91 : 01,09 : 0x01,0x09 
rend_145: dl rend_145_0,rend_145_1,rend_145_2,rend_145_3
rend_145_0:
	jp render_scene_return
rend_145_1:
	jp render_scene_return
rend_145_2:
	ld hl,0x0901FE ; BUF_17_09
	call render_panel
	jp render_scene_return
rend_145_3:
	ld hl,0x0001F5 ; BUF_17_00
	call render_panel
	ld hl,0x03018F ; BUF_14_03
	call render_panel
	ld hl,0x0B0196 ; BUF_14_14
	call render_panel
	ld hl,0x0C0196 ; BUF_14_14
	call render_panel
	jp render_scene_return
; 0x92 : 02,09 : 0x02,0x09 
rend_146: dl rend_146_0,rend_146_1,rend_146_2,rend_146_3
rend_146_0:
	jp render_scene_return
rend_146_1:
	jp render_scene_return
rend_146_2:
	ld hl,0x090109 ; BUF_10_09
	call render_panel
	jp render_scene_return
rend_146_3:
	ld hl,0x0101F6 ; BUF_17_01
	call render_panel
	ld hl,0x040190 ; BUF_14_04
	call render_panel
	ld hl,0x0A01FF ; BUF_17_14
	call render_panel
	ld hl,0x0C0196 ; BUF_14_14
	call render_panel
	ld hl,0x0D0196 ; BUF_14_14
	call render_panel
	jp render_scene_return
; 0x93 : 03,09 : 0x03,0x09 
rend_147: dl rend_147_0,rend_147_1,rend_147_2,rend_147_3
rend_147_0:
	jp render_scene_return
rend_147_1:
	jp render_scene_return
rend_147_2:
	ld hl,0x0901FE ; BUF_17_09
	call render_panel
	jp render_scene_return
rend_147_3:
	ld hl,0x0201F7 ; BUF_17_02
	call render_panel
	ld hl,0x0A010A ; BUF_10_14
	call render_panel
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x0D0196 ; BUF_14_14
	call render_panel
	ld hl,0x0E0196 ; BUF_14_14
	call render_panel
	jp render_scene_return
; 0x94 : 04,09 : 0x04,0x09 
rend_148: dl rend_148_0,rend_148_1,rend_148_2,rend_148_3
rend_148_0:
	jp render_scene_return
rend_148_1:
	jp render_scene_return
rend_148_2:
	ld hl,0x0801FD ; BUF_17_08
	call render_panel
	ld hl,0x1201FF ; BUF_17_14
	call render_panel
	jp render_scene_return
rend_148_3:
	ld hl,0x0301F8 ; BUF_17_03
	call render_panel
	ld hl,0x0A01FF ; BUF_17_14
	call render_panel
	ld hl,0x0B010A ; BUF_10_14
	call render_panel
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E0196 ; BUF_14_14
	call render_panel
	ld hl,0x0F0196 ; BUF_14_14
	call render_panel
	jp render_scene_return
; 0x95 : 05,09 : 0x05,0x09 
rend_149: dl rend_149_0,rend_149_1,rend_149_2,rend_149_3
rend_149_0:
	jp render_scene_return
rend_149_1:
	jp render_scene_return
rend_149_2:
	ld hl,0x080108 ; BUF_10_08
	call render_panel
	ld hl,0x1A0207 ; BUF_17_26
	call render_panel
	jp render_scene_return
rend_149_3:
	ld hl,0x0401F9 ; BUF_17_04
	call render_panel
	ld hl,0x050191 ; BUF_14_05
	call render_panel
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x0C010A ; BUF_10_14
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F0196 ; BUF_14_14
	call render_panel
	ld hl,0x100196 ; BUF_14_14
	call render_panel
	ld hl,0x130200 ; BUF_17_19
	call render_panel
	jp render_scene_return
; 0x96 : 06,09 : 0x06,0x09 
rend_150: dl rend_150_0,rend_150_1,rend_150_2,rend_150_3
rend_150_0:
	jp render_scene_return
rend_150_1:
	jp render_scene_return
rend_150_2:
	ld hl,0x0801FD ; BUF_17_08
	call render_panel
	ld hl,0x1A0112 ; BUF_10_26
	call render_panel
	jp render_scene_return
rend_150_3:
	ld hl,0x060192 ; BUF_14_06
	call render_panel
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x100196 ; BUF_14_14
	call render_panel
	ld hl,0x110196 ; BUF_14_14
	call render_panel
	ld hl,0x140201 ; BUF_17_20
	call render_panel
	ld hl,0x1B0208 ; BUF_17_30
	call render_panel
	jp render_scene_return
; 0x97 : 07,09 : 0x07,0x09 
rend_151: dl rend_151_0,rend_151_1,rend_151_2,rend_151_3
rend_151_0:
	jp render_scene_return
rend_151_1:
	jp render_scene_return
rend_151_2:
	ld hl,0x080108 ; BUF_10_08
	call render_panel
	ld hl,0x1A0207 ; BUF_17_26
	call render_panel
	jp render_scene_return
rend_151_3:
	ld hl,0x070193 ; BUF_14_07
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x110196 ; BUF_14_14
	call render_panel
	ld hl,0x120196 ; BUF_14_14
	call render_panel
	ld hl,0x150202 ; BUF_17_21
	call render_panel
	ld hl,0x1B0113 ; BUF_10_30
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	jp render_scene_return
; 0x98 : 08,09 : 0x08,0x09 
rend_152: dl rend_152_0,rend_152_1,rend_152_2,rend_152_3
rend_152_0:
	ld hl,0x00018C ; BUF_14_00
	call render_panel
	jp render_scene_return
rend_152_1:
	jp render_scene_return
rend_152_2:
	ld hl,0x0801FD ; BUF_17_08
	call render_panel
	ld hl,0x1A0112 ; BUF_10_26
	call render_panel
	jp render_scene_return
rend_152_3:
	ld hl,0x080194 ; BUF_14_08
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x120196 ; BUF_14_14
	call render_panel
	ld hl,0x160203 ; BUF_17_22
	call render_panel
	ld hl,0x1B0208 ; BUF_17_30
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	jp render_scene_return
; 0x99 : 09,09 : 0x09,0x09 
rend_153: dl rend_153_0,rend_153_1,rend_153_2,rend_153_3
rend_153_0:
	ld hl,0x00018C ; BUF_14_00
	call render_panel
	jp render_scene_return
rend_153_1:
	jp render_scene_return
rend_153_2:
	ld hl,0x1A0207 ; BUF_17_26
	call render_panel
	jp render_scene_return
rend_153_3:
	ld hl,0x090195 ; BUF_14_09
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x10010A ; BUF_10_14
	call render_panel
	ld hl,0x1101FF ; BUF_17_14
	call render_panel
	ld hl,0x1B0113 ; BUF_10_30
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	jp render_scene_return
; 0x9A : 10,09 : 0x0A,0x09 
rend_154: dl rend_154_0,rend_154_1,rend_154_2,rend_154_3
rend_154_0:
	jp render_scene_return
rend_154_1:
	jp render_scene_return
rend_154_2:
	jp render_scene_return
rend_154_3:
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x11010A ; BUF_10_14
	call render_panel
	ld hl,0x1201FF ; BUF_17_14
	call render_panel
	ld hl,0x1B0208 ; BUF_17_30
	call render_panel
	ld hl,0x1C0113 ; BUF_10_30
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	jp render_scene_return
; 0x9B : 11,09 : 0x0B,0x09 
rend_155: dl rend_155_0,rend_155_1,rend_155_2,rend_155_3
rend_155_0:
	ld hl,0x0001F5 ; BUF_17_00
	call render_panel
	jp render_scene_return
rend_155_1:
	jp render_scene_return
rend_155_2:
	jp render_scene_return
rend_155_3:
	ld hl,0x0B010A ; BUF_10_14
	call render_panel
	ld hl,0x1101FF ; BUF_17_14
	call render_panel
	ld hl,0x12010A ; BUF_10_14
	call render_panel
	ld hl,0x1C0208 ; BUF_17_30
	call render_panel
	ld hl,0x1D0113 ; BUF_10_30
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	jp render_scene_return
; 0x9C : 12,09 : 0x0C,0x09 
rend_156: dl rend_156_0,rend_156_1,rend_156_2,rend_156_3
rend_156_0:
	ld hl,0x000100 ; BUF_10_00
	call render_panel
	jp render_scene_return
rend_156_1:
	jp render_scene_return
rend_156_2:
	jp render_scene_return
rend_156_3:
	ld hl,0x0C010A ; BUF_10_14
	call render_panel
	ld hl,0x1D0208 ; BUF_17_30
	call render_panel
	ld hl,0x1E0113 ; BUF_10_30
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x200113 ; BUF_10_30
	call render_panel
	ld hl,0x210208 ; BUF_17_30
	call render_panel
	jp render_scene_return
; 0x9D : 13,09 : 0x0D,0x09 
rend_157: dl rend_157_0,rend_157_1,rend_157_2,rend_157_3
rend_157_0:
	ld hl,0x130200 ; BUF_17_19
	call render_panel
	jp render_scene_return
rend_157_1:
	jp render_scene_return
rend_157_2:
	jp render_scene_return
rend_157_3:
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x1E0208 ; BUF_17_30
	call render_panel
	ld hl,0x1F0113 ; BUF_10_30
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x210113 ; BUF_10_30
	call render_panel
	jp render_scene_return
; 0x9E : 14,09 : 0x0E,0x09 
rend_158: dl rend_158_0,rend_158_1,rend_158_2,rend_158_3
rend_158_0:
	ld hl,0x0101F6 ; BUF_17_01
	call render_panel
	ld hl,0x13010B ; BUF_10_19
	call render_panel
	jp render_scene_return
rend_158_1:
	jp render_scene_return
rend_158_2:
	jp render_scene_return
rend_158_3:
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x170204 ; BUF_17_23
	call render_panel
	ld hl,0x1F0208 ; BUF_17_30
	call render_panel
	ld hl,0x200113 ; BUF_10_30
	call render_panel
	ld hl,0x210208 ; BUF_17_30
	call render_panel
	jp render_scene_return
; 0x9F : 15,09 : 0x0F,0x09 
rend_159: dl rend_159_0,rend_159_1,rend_159_2,rend_159_3
rend_159_0:
	ld hl,0x010101 ; BUF_10_01
	call render_panel
	ld hl,0x130200 ; BUF_17_19
	call render_panel
	jp render_scene_return
rend_159_1:
	jp render_scene_return
rend_159_2:
	jp render_scene_return
rend_159_3:
	ld hl,0x050105 ; BUF_10_05
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x180205 ; BUF_17_24
	call render_panel
	ld hl,0x200208 ; BUF_17_30
	call render_panel
	ld hl,0x210113 ; BUF_10_30
	call render_panel
	jp render_scene_return
; 0xA0 : 00,10 : 0x00,0x0A 
rend_160:
; 0xA1 : 01,10 : 0x01,0x0A 
rend_161:
; 0xA2 : 02,10 : 0x02,0x0A 
rend_162:
; 0xA3 : 03,10 : 0x03,0x0A 
rend_163:
; 0xA4 : 04,10 : 0x04,0x0A 
rend_164: dl rend_164_0,rend_164_1,rend_164_2,rend_164_3
rend_164_0:
	jp render_scene_return
rend_164_1:
	jp render_scene_return
rend_164_2:
	ld hl,0x0901FE ; BUF_17_09
	call render_panel
	jp render_scene_return
rend_164_3:
	ld hl,0x0001F5 ; BUF_17_00
	call render_panel
	jp render_scene_return
; 0xA5 : 05,10 : 0x05,0x0A 
rend_165: dl rend_165_0,rend_165_1,rend_165_2,rend_165_3
rend_165_0:
	jp render_scene_return
rend_165_1:
	jp render_scene_return
rend_165_2:
	ld hl,0x090109 ; BUF_10_09
	call render_panel
	jp render_scene_return
rend_165_3:
	ld hl,0x0101F6 ; BUF_17_01
	call render_panel
	ld hl,0x0A01FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xA6 : 06,10 : 0x06,0x0A 
rend_166: dl rend_166_0,rend_166_1,rend_166_2,rend_166_3
rend_166_0:
	jp render_scene_return
rend_166_1:
	jp render_scene_return
rend_166_2:
	ld hl,0x0901FE ; BUF_17_09
	call render_panel
	jp render_scene_return
rend_166_3:
	ld hl,0x0201F7 ; BUF_17_02
	call render_panel
	ld hl,0x0A010A ; BUF_10_14
	call render_panel
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xA7 : 07,10 : 0x07,0x0A 
rend_167: dl rend_167_0,rend_167_1,rend_167_2,rend_167_3
rend_167_0:
	jp render_scene_return
rend_167_1:
	jp render_scene_return
rend_167_2:
	ld hl,0x090109 ; BUF_10_09
	call render_panel
	jp render_scene_return
rend_167_3:
	ld hl,0x0301F8 ; BUF_17_03
	call render_panel
	ld hl,0x0A01FF ; BUF_17_14
	call render_panel
	ld hl,0x0B010A ; BUF_10_14
	call render_panel
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xA8 : 08,10 : 0x08,0x0A 
rend_168: dl rend_168_0,rend_168_1,rend_168_2,rend_168_3
rend_168_0:
	jp render_scene_return
rend_168_1:
	jp render_scene_return
rend_168_2:
	ld hl,0x0901FE ; BUF_17_09
	call render_panel
	jp render_scene_return
rend_168_3:
	ld hl,0x0401F9 ; BUF_17_04
	call render_panel
	ld hl,0x0A010A ; BUF_10_14
	call render_panel
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x0C010A ; BUF_10_14
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xA9 : 09,10 : 0x09,0x0A 
rend_169: dl rend_169_0,rend_169_1,rend_169_2,rend_169_3
rend_169_0:
	jp render_scene_return
rend_169_1:
	jp render_scene_return
rend_169_2:
	jp render_scene_return
rend_169_3:
	ld hl,0x0A01FF ; BUF_17_14
	call render_panel
	ld hl,0x0B010A ; BUF_10_14
	call render_panel
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xAA : 10,10 : 0x0A,0x0A 
rend_170: dl rend_170_0,rend_170_1,rend_170_2,rend_170_3
rend_170_0:
	jp render_scene_return
rend_170_1:
	jp render_scene_return
rend_170_2:
	jp render_scene_return
rend_170_3:
	ld hl,0x0B01FF ; BUF_17_14
	call render_panel
	ld hl,0x0C010A ; BUF_10_14
	call render_panel
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xAB : 11,10 : 0x0B,0x0A 
rend_171: dl rend_171_0,rend_171_1,rend_171_2,rend_171_3
rend_171_0:
	jp render_scene_return
rend_171_1:
	jp render_scene_return
rend_171_2:
	jp render_scene_return
rend_171_3:
	ld hl,0x0C01FF ; BUF_17_14
	call render_panel
	ld hl,0x0D010A ; BUF_10_14
	call render_panel
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xAC : 12,10 : 0x0C,0x0A 
rend_172: dl rend_172_0,rend_172_1,rend_172_2,rend_172_3
rend_172_0:
	jp render_scene_return
rend_172_1:
	jp render_scene_return
rend_172_2:
	jp render_scene_return
rend_172_3:
	ld hl,0x0D01FF ; BUF_17_14
	call render_panel
	ld hl,0x0E010A ; BUF_10_14
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x10010A ; BUF_10_14
	call render_panel
	ld hl,0x1101FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xAD : 13,10 : 0x0D,0x0A 
rend_173: dl rend_173_0,rend_173_1,rend_173_2,rend_173_3
rend_173_0:
	jp render_scene_return
rend_173_1:
	jp render_scene_return
rend_173_2:
	jp render_scene_return
rend_173_3:
	ld hl,0x0E01FF ; BUF_17_14
	call render_panel
	ld hl,0x0F010A ; BUF_10_14
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x11010A ; BUF_10_14
	call render_panel
	ld hl,0x1201FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xAE : 14,10 : 0x0E,0x0A 
rend_174: dl rend_174_0,rend_174_1,rend_174_2,rend_174_3
rend_174_0:
	ld hl,0x0001F5 ; BUF_17_00
	call render_panel
	jp render_scene_return
rend_174_1:
	jp render_scene_return
rend_174_2:
	jp render_scene_return
rend_174_3:
	ld hl,0x0501FA ; BUF_17_05
	call render_panel
	ld hl,0x0F01FF ; BUF_17_14
	call render_panel
	ld hl,0x10010A ; BUF_10_14
	call render_panel
	ld hl,0x1101FF ; BUF_17_14
	call render_panel
	ld hl,0x12010A ; BUF_10_14
	call render_panel
	jp render_scene_return
; 0xAF : 15,10 : 0x0F,0x0A 
rend_175: dl rend_175_0,rend_175_1,rend_175_2,rend_175_3
rend_175_0:
	ld hl,0x000100 ; BUF_10_00
	call render_panel
	jp render_scene_return
rend_175_1:
	jp render_scene_return
rend_175_2:
	jp render_scene_return
rend_175_3:
	ld hl,0x0601FB ; BUF_17_06
	call render_panel
	ld hl,0x1001FF ; BUF_17_14
	call render_panel
	ld hl,0x11010A ; BUF_10_14
	call render_panel
	ld hl,0x1201FF ; BUF_17_14
	call render_panel
	jp render_scene_return
; 0xB0 : 00,11 : 0x00,0x0B 
rend_176:
; 0xB1 : 01,11 : 0x01,0x0B 
rend_177:
; 0xB2 : 02,11 : 0x02,0x0B 
rend_178:
; 0xB3 : 03,11 : 0x03,0x0B 
rend_179:
; 0xB4 : 04,11 : 0x04,0x0B 
rend_180:
; 0xB5 : 05,11 : 0x05,0x0B 
rend_181:
; 0xB6 : 06,11 : 0x06,0x0B 
rend_182:
; 0xB7 : 07,11 : 0x07,0x0B 
rend_183:
; 0xB8 : 08,11 : 0x08,0x0B 
rend_184:
; 0xB9 : 09,11 : 0x09,0x0B 
rend_185:
; 0xBA : 10,11 : 0x0A,0x0B 
rend_186:
; 0xBB : 11,11 : 0x0B,0x0B 
rend_187:
; 0xBC : 12,11 : 0x0C,0x0B 
rend_188:
; 0xBD : 13,11 : 0x0D,0x0B 
rend_189:
; 0xBE : 14,11 : 0x0E,0x0B 
rend_190:
; 0xBF : 15,11 : 0x0F,0x0B 
rend_191:
; 0xC0 : 00,12 : 0x00,0x0C 
rend_192:
; 0xC1 : 01,12 : 0x01,0x0C 
rend_193:
; 0xC2 : 02,12 : 0x02,0x0C 
rend_194:
; 0xC3 : 03,12 : 0x03,0x0C 
rend_195:
; 0xC4 : 04,12 : 0x04,0x0C 
rend_196:
; 0xC5 : 05,12 : 0x05,0x0C 
rend_197:
; 0xC6 : 06,12 : 0x06,0x0C 
rend_198:
; 0xC7 : 07,12 : 0x07,0x0C 
rend_199:
; 0xC8 : 08,12 : 0x08,0x0C 
rend_200:
; 0xC9 : 09,12 : 0x09,0x0C 
rend_201:
; 0xCA : 10,12 : 0x0A,0x0C 
rend_202:
; 0xCB : 11,12 : 0x0B,0x0C 
rend_203:
; 0xCC : 12,12 : 0x0C,0x0C 
rend_204:
; 0xCD : 13,12 : 0x0D,0x0C 
rend_205:
; 0xCE : 14,12 : 0x0E,0x0C 
rend_206:
; 0xCF : 15,12 : 0x0F,0x0C 
rend_207:
; 0xD0 : 00,13 : 0x00,0x0D 
rend_208:
; 0xD1 : 01,13 : 0x01,0x0D 
rend_209:
; 0xD2 : 02,13 : 0x02,0x0D 
rend_210:
; 0xD3 : 03,13 : 0x03,0x0D 
rend_211:
; 0xD4 : 04,13 : 0x04,0x0D 
rend_212:
; 0xD5 : 05,13 : 0x05,0x0D 
rend_213:
; 0xD6 : 06,13 : 0x06,0x0D 
rend_214:
; 0xD7 : 07,13 : 0x07,0x0D 
rend_215:
; 0xD8 : 08,13 : 0x08,0x0D 
rend_216:
; 0xD9 : 09,13 : 0x09,0x0D 
rend_217:
; 0xDA : 10,13 : 0x0A,0x0D 
rend_218:
; 0xDB : 11,13 : 0x0B,0x0D 
rend_219:
; 0xDC : 12,13 : 0x0C,0x0D 
rend_220:
; 0xDD : 13,13 : 0x0D,0x0D 
rend_221:
; 0xDE : 14,13 : 0x0E,0x0D 
rend_222:
; 0xDF : 15,13 : 0x0F,0x0D 
rend_223:
; 0xE0 : 00,14 : 0x00,0x0E 
rend_224:
; 0xE1 : 01,14 : 0x01,0x0E 
rend_225:
; 0xE2 : 02,14 : 0x02,0x0E 
rend_226:
; 0xE3 : 03,14 : 0x03,0x0E 
rend_227:
; 0xE4 : 04,14 : 0x04,0x0E 
rend_228:
; 0xE5 : 05,14 : 0x05,0x0E 
rend_229:
; 0xE6 : 06,14 : 0x06,0x0E 
rend_230:
; 0xE7 : 07,14 : 0x07,0x0E 
rend_231:
; 0xE8 : 08,14 : 0x08,0x0E 
rend_232:
; 0xE9 : 09,14 : 0x09,0x0E 
rend_233:
; 0xEA : 10,14 : 0x0A,0x0E 
rend_234:
; 0xEB : 11,14 : 0x0B,0x0E 
rend_235:
; 0xEC : 12,14 : 0x0C,0x0E 
rend_236:
; 0xED : 13,14 : 0x0D,0x0E 
rend_237:
; 0xEE : 14,14 : 0x0E,0x0E 
rend_238:
; 0xEF : 15,14 : 0x0F,0x0E 
rend_239:
; 0xF0 : 00,15 : 0x00,0x0F 
rend_240:
; 0xF1 : 01,15 : 0x01,0x0F 
rend_241:
; 0xF2 : 02,15 : 0x02,0x0F 
rend_242:
; 0xF3 : 03,15 : 0x03,0x0F 
rend_243:
; 0xF4 : 04,15 : 0x04,0x0F 
rend_244:
; 0xF5 : 05,15 : 0x05,0x0F 
rend_245:
; 0xF6 : 06,15 : 0x06,0x0F 
rend_246:
; 0xF7 : 07,15 : 0x07,0x0F 
rend_247:
; 0xF8 : 08,15 : 0x08,0x0F 
rend_248:
; 0xF9 : 09,15 : 0x09,0x0F 
rend_249:
; 0xFA : 10,15 : 0x0A,0x0F 
rend_250:
; 0xFB : 11,15 : 0x0B,0x0F 
rend_251:
; 0xFC : 12,15 : 0x0C,0x0F 
rend_252:
; 0xFD : 13,15 : 0x0D,0x0F 
rend_253:
; 0xFE : 14,15 : 0x0E,0x0F 
rend_254:
; 0xFF : 15,15 : 0x0F,0x0F 
rend_255:
