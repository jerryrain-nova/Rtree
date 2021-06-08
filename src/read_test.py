bits = [12441, 12462, 56649, 56670, 809417, 809437, 884388, 884408, 966219, 966239, 1073398, 1073418, 1172364, 1172384, 1233360, 1233380, 1427410, 1427430, 1608705, 1608725, 1855855, 1855875, 1914562, 1914582, 1959946, 1959966, 2011715, 2011735, 2209812, 2209832, 2430560, 2430580, 2462878, 2462898, 2549702, 2549723, 2551281, 2551302, 2638306, 2638326, 2891567, 2891587, 2998776, 2998796, 3137823, 3137843, 3174262, 3174283, 3355202, 3355222, 3470737, 3470758, 3504330, 3504350, 3540204, 3540224, 3633239, 3633259, 3668857, 3668877, 3803055, 3803075, 3803378, 3803398, 3935597, 3935618, 3940865, 3940886, 4025919, 4025939, 4084390, 4084411, 4289404, 4289425, 4317849, 4317869, 4328022, 4328042, 4445943, 4445963, 4467496, 4467517, 4488000, 4488020, 4511752, 4511772, 4711412, 4711433, 4725380, 4725401, 4734516, 4734536, 4939441, 4939461, 4946276, 4946296, 5020636, 5020657, 5044183, 5044203, 5107523, 5107544, 5217058, 5217079, 6024815, 6024836, 6303781, 6303802, 6413640, 6413661, 6541129, 6541149, 6629875, 6629896, 6630368, 6630389, 6701845, 6701865, 6738296, 6738317, 6889414, 6889435, 6897177, 6897198, 6906497, 6906518, 6913675, 6913695, 7143580, 7143600, 7189391, 7189412, 7192732, 7192752, 7206640, 7206660, 7405491, 7405512, 7466545, 7466565, 7521870, 7521891, 7729240, 7729260, 7794295, 7794315, 7835733, 7835753, 8354824, 8354845, 8632972, 8632992, 8659641, 8659662, 8851189, 8851210, 8917451, 8917472, 9018665, 9018685, 9453979, 9453999, 9703107, 9703128, 10007244, 10007264, 10152346, 10152367, 10281805, 10281825, 10374700, 10374721, 10384018, 10384038, 10593042, 10593063, 10606766, 10606787, 10620730, 10620751, 10632649, 10632669, 10743244, 10743265, 10892631, 10892652, 10902677, 10902698, 11255482, 11255502, 11326289, 11326310, 11496552, 11496572, 11522679, 11522700, 11558175, 11558195, 11634071, 11634091, 12081114, 12081135, 12316112, 12316133, 12345226, 12345247, 12526716, 12526736, 12590506, 12590527, 12595598, 12595619, 12675119, 12675140, 12756401, 12756422, 12934797, 12934818, 13050080, 13050101, 13099265, 13099285, 13153495, 13153516, 13390849, 13390869, 13793485, 13793505, 13808119, 13808140, 13930719, 13930740, 14260493, 14260513, 14271835, 14271855, 14338165, 14338186, 14692134, 14692155, 14790750, 14790770, 14831256, 14831277, 15221690, 15221711, 15700424, 15700444, 16160511, 16160532, 16337539, 16337559, 16644824, 16644844, 16741678, 16741698, 16840159, 16840180, 17163828, 17163848, 17281210, 17281231, 17709884, 17709905, 17774032, 17774052, 17922113, 17922134, 17971413, 17971433, 18040205, 18040226, 18577811, 18577831, 18645023, 18645043, 18651552, 18651573, 18889016, 18889036, 19060889, 19060909, 19096724, 19096745, 19338436, 19338456, 19795867, 19795888, 20039877, 20039899, 20096760, 20096781, 20278936, 20278957, 20361731, 20361752, 20371460, 20371481, 20454126, 20454147, 20483530, 20483551, 20575702, 20575723, 20635769, 20635790, 20644040, 20644061, 20715034, 20715056]
index = "C:/Users/chenyujie/Desktop/Test/FP200000289TR_A2_1M.index"
data = "C:/Users/chenyujie/Desktop/Test/FP200000289TR_A2_1M.data"

dt = open(data, 'r')
gt = []
for i in range(0, len(bits), 2):
    dt.seek(bits[i])
    gt.append(dt.read(bits[i+1]-bits[i]).strip(','))
print(len(gt))
print(len(list(set(gt))))