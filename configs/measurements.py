# SMPL measurements - uses SMPL vertex IDs and joint IDs as measurement end-point definitions.
JOINT_LENGTH_MEAS_NAMES = [
    'Torso_Length',
    'L_Thigh_Length',
    'R_Thigh_Length',
    'L_Calf_Length',
    'R_Calf_Length',
    'L_Arm_Length',
    'R_Arm_Length',
]
JOINT_LENGTH_MEAS_INDEXES = [
    [0, 15],   # Hip to Top of Neck = Torso
    [1, 4],    # L Hip to L Knee = L Thigh
    [2, 5],    # R Hip to R Knee = R Thigh
    [4, 7],    # L Knee to L Ankle = L Calf
    [5, 8],    # R Knee to R Ankle = R Calf
    [16, 20],  # L Shoulder to L Wrist = L Arm
    [17, 21]  # R Shoulder to R Wrist = R Arm
]
VERTEX_CIRCUMFERENCE_MEAS_NAMES = [
    'L_Forearm_Circum',
    'R_Forearm_Circum',
    'L_Upper_Arm_Circum',
    'R_Upper_Arm_Circum',
    'L_Calf_Circum',
    'R_Calf_Circum',
    'L_Lower_Thigh_Circum',
    'R_Lower_Thigh_Circum',
    'L_Upper_Thigh_Circum',
    'R_Upper_Thigh_Circum',
    'Neck_Circum'
]
VERTEX_CIRCUMFERENCE_MEAS_INDEXES = [
    [1557, 1558, 1587, 1554, 1553, 1727, 1583, 1584, 1689, 1687, 1686, 1590, 1591, 1548, 1547, 1551],  # Left Forearm
    [5027, 5028, 5020, 5018, 5017, 5060, 5061, 5157, 5156, 5159, 5053, 5054, 5196, 5024, 5023, 5057],  # Right Forearm
    [628, 627, 789, 1311, 1315, 1379, 1378, 1394, 1393, 1389, 1388, 1233, 1232, 1385, 1381, 1382, 1397, 1396],  # Left Upper Arm
    [4117, 4277, 4791, 4794, 4850, 4851, 4865, 4866, 4862, 4863, 4716, 4717, 4859, 4856, 4855, 4870, 4871, 4116],  # Right Upper Arm
    [1074, 1077, 1470, 1094, 1095, 1473, 1465, 1466, 1108, 1111, 1530, 1089, 1086, 1154, 1372],  # Left Calf
    [4583, 4580, 4943, 4561, 4560, 4845, 4640, 4572, 4573, 5000, 4595, 4594, 4940, 4938, 4946],  # Right Calf
    [1041, 1147, 1171, 1172, 1029, 1030, 1167, 1033, 1034, 1035, 1037, 1036, 1038, 1040, 1039, 1520, 1042],  # Left Lower Thigh
    [4528, 4632, 4657, 4660, 4515, 4518, 4653, 4519, 4520, 4521, 4522, 4523, 4524, 4525, 4526, 4991, 4527],  # Right Lower Thigh
    [910, 1365, 907, 906, 957, 904, 905, 903, 901, 962, 898, 899, 934, 935, 1453, 964, 909, 910],  # Left Upper Thigh
    [4397, 4396, 4838, 4393, 4392, 4443, 4391, 4390, 4388, 4387, 4448, 4386, 4385, 4422, 4421, 4926, 4449],  # Right Upper Thigh
    [3050, 3839, 3796, 3797, 3662, 3663, 3810, 3718, 3719, 3723, 3724, 3768, 3918, 460, 423, 257, 212, 213, 209, 206, 298, 153, 150, 285, 284, 334],  # Neck
]
VERTEX_LENGTH_MEAS_NAMES = [
    'Chest_Width',
    'Stomach_Width',
    'Hip_Width',
    'Abdomen_Width',
    'Chest_Depth',
    'Stomach_Depth',
    'Hip_Depth',
    'Abdomen_Depth',
    'Head_Width',
    'Head_Height',
    'Head_Depth',
    'Underbust_Depth',
    'Shoulder_Width',
]
VERTEX_LENGTH_MEAS_INDEXES = [
    [4226, 738],   # Chest Width
    [4804, 1323],  # Waist/Stomach Width
    [6550, 3129],  # Hip Width
    [1794, 5256],  # Abdomen Width
    [3076, 3015],  # Chest Depth
    [3509, 3502],  # Waist/Stomach Depth
    [3145, 3141],  # Hip Depth
    [3507, 3159],  # Abdomen Depth
    [368, 3872],  # Head Width
    [412, 3058],  # Head Height
    [457, 3165],  # Head Depth
    [1329, 3017],  # Underbust Depth
    [1509, 4982],  # Shoulder Width
]
ALL_MEAS_NAMES = JOINT_LENGTH_MEAS_NAMES + VERTEX_LENGTH_MEAS_NAMES + VERTEX_CIRCUMFERENCE_MEAS_NAMES
ALL_MEAS_NAMES_NO_SYMM = [name.replace('L_', '') for name in ALL_MEAS_NAMES if not name.startswith('R_')]
NUMBER_OF_MEAS_TYPES = len(ALL_MEAS_NAMES)
NUMBER_OF_MEAS_TYPES_NO_SYMM = len(ALL_MEAS_NAMES_NO_SYMM)