#############################################
# COPY AND PASTE FROM HERE (including this) #
#############################################
 
# Ice Dodo Blender UNOFFICIAL Compiler Version 8.2 (applepear + awehero)
 
### IMPORT LIBRARIES AND FUNCTIONS
import bpy
import bmesh
bpy.ops.object.select_all( action = 'SELECT' )
bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' )
bpy.ops.object.select_all( action = 'DESELECT' )
 
try:
    def dp(xs):
        def fn(x):
            return round(x*10**2)
        return list(map(fn, list(xs)))
 
    def print(data):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'CONSOLE':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")
 
    for k in range(30):
        print("-")
 
 
    ### DEPRECATION NOTICE
    deprecation_mapping = {
        'ax': '"ax" has been renamed to "gx"',
        'ay': '"ay" has been renamed to "gy"',
        'az': '"az" has been renamed to "gz"',
        'pm': '"pm", "cm" and "sm" all have been renamed to "mat", which stands for material.',
        'cm': '"pm", "cm" and "sm" all have been renamed to "mat", which stands for material.',
        'sm': '"pm", "cm" and "sm" all have been renamed to "mat", which stands for material.'
    }
 
 
    ### STANDARDIZE MESHES
    def standardize(item):
        obj = item['obj']
        obj.scale = list(obj.scale)
        obj.rotation_euler = list(obj.rotation_euler)
 
        if item['type'] == "A_Section":
            if list(obj.scale)[0] != 1000 or list(obj.scale)[2] != 1 or list(obj.location)[0] != 0 or list(obj.location)[2] != -21 or list(obj.rotation_euler) != [0,0,0]:
                print("Note: Plane has been standard-ized.")
                obj.scale[0] = 1000;
                obj.scale[2] = 1;
                obj.location[0] = 0;
                obj.location[2] = -21;
                obj.rotation_euler = [0,0,0]
        elif item['type'] == "B_Platform":
            pass;
        elif item['type'] == "C_Cone":
            if list(obj.scale) != [1,1,1] or list(obj.rotation_euler) != [0,0,0]:
                print("Note: Cone has been standard-ized.")
                obj.scale = [1,1,1]
                obj.rotation_euler = [0,0,0]
        elif item['type'] == "D_End":
            if list(obj.scale) != [3,3,3] or list(obj.rotation_euler) != [0,0,0]:
                print("Note: Ending has been standard-ized.")
                obj.scale = [3,3,3]
                obj.rotation_euler = [0,0,0]
        elif item['type'] == "E_Cylinder":
            if list(obj.scale)[0] != list(obj.scale)[1]:
                print("Note: Cylinder has been standard-ized.")
                if float(obj.scale[0]) > float(obj.scale[1]):
                    obj.scale[1] = obj.scale[0]
                else:
                    obj.scale[0] = obj.scale[1]
        elif item['type'] == "F_Sphere":
            if max(list(obj.scale)) != min(list(obj.scale)) or list(obj.rotation_euler) != [0,0,0]:
                print("Note: Sphere has been standard-ized.")
                obj.scale[0] = max(obj.scale)
                obj.scale[1] = max(obj.scale)
                obj.scale[2] = max(obj.scale)
                obj.rotation_euler = [0,0,0]
        elif item['type'] == "G_Monkey":
            if list(obj.scale) != [10,10,10] or list(obj.rotation_euler) != [0,0,0]:
                print("Note: Monkey has been standard-ized.")
                obj.scale = [10,10,10]
                obj.rotation_euler = [0,0,0]
 
    ### READ BLENDER DATA
    use_arr = []
    use_index = 0;
    items = []
    iter_num = 0
    for obj in bpy.data.objects:
        item = {
            'err': ['Unrecognized object type. Please delete this object.'],
            'obj': obj,
            'name': obj.name
        }
        obj.rotation_mode = 'XYZ'
        if obj.type == "MESH":
            iter_num += 1
            vert_count = len(obj.data.vertices)
            vert_to_type = {'4':'A_Section','8':'B_Platform','33':'C_Cone', '482':'D_End', '64': 'E_Cylinder', '42':'F_Sphere', '507': 'G_Monkey', '121': 'H_Grid', '576': "I_Donut"}
            if vert_count in list(map(int, list(vert_to_type.keys()))):
                # normalize mesh
                standardize({
                    'obj': obj,
                    'type': vert_to_type[str(vert_count)]
                })
                # add data
                item = {
                    'err': [],
                    'obj': obj,
                    'name': obj.name,
                    'type': vert_to_type[str(vert_count)],
                    'siz': list(map(abs, dp(list(obj.scale)))),
                    'pos': dp(list(obj.location)),
                    'rot': dp(list(obj.rotation_euler)),
                    'eff': 'none'
                }
                item['pos'][0] += (iter_num % 8) * 0.007
                item['pos'][1] += (iter_num % 8) * 0.007
                item['pos'][2] += (iter_num % 8) * 0.007
                if (item['type'] == "G_Monkey"):
                    use_arr.append([])
        items.append(item)
 
 
    def positive_val(x):
        try:
            if float(x) >= 0:
                return True;
            else:
                return False
        except Exception as e:
            pass;
 
    def decimal_val(x):
        try:
            if float(x) * float(x) >= 0:
                return True;
            else:
                return False
        except Exception as e:
            pass;
 
    def decimal_map(x):
        return round(float(x), 3)
 
    def hex_val(x):
        if len(x) != 7:
            return False;
        if x[0] != "#":
            return False;
        for c in list(x[1:]):
            if c.lower() not in list("0123456789abcdef"):
                return False;
        return True
 
    def dec_or_hex_val(x):
        if decimal_val(x):
            return True;
        elif hex_val(x):
            return True;
        else:
            return False
 
    def dec_or_hex_map(x):
        if decimal_val(x):
            return decimal_map(x);
        elif hex_val(x):
            return hex_map(x);
        else:
            return x
 
    def hex_map(x):
        return x.lower()[1:];
 
    def use_name_val(x):
        allowed_chars = list("abcdefghijklmnopqrstuvwxyz_0123456789")
        for char in list(x):
            if char not in allowed_chars:
                return False
        return True
 
    ### SPECIAL EFFECTS
    effects = [
        {
            'ids': ["id"],
            'type': ['A_Section', 'G_Monkey', 'B_Platform', 'C_Cone', 'D_End', 'E_Cylinder', 'G_Monkey', "F_Sphere"],
            'map': lambda x: round(float(x)),
            'val': decimal_val
        },
        {
            'ids': ["gravityX", "gx"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["gravityY", "gy"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["gravityZ", "gz"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["tiltX", "tx"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["tiltY", "ty"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["tiltZ", "tz"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["turn", "t", "turn"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["speed", "s", "speed"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["fov", "fov"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["message", "msg"],
            'type': ['A_Section', 'G_Monkey'],
            'map': lambda x: str(x),
            'val': decimal_val
        },
        {
            'ids': ["dodox", "dx"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["dodoy", "dy"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["dodoz", "dz"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["m", "material", "mat"],
            'type': ['B_Platform', 'E_Cylinder', 'C_Cone', 'F_Sphere', 'G_Monkey'],
            'map': dec_or_hex_map,
            'val': dec_or_hex_val
        },
        {
            'ids': ["opacity", "o"],
            'type': ['B_Platform', 'E_Cylinder', 'C_Cone', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["air", "air"],
            'type': ['B_Platform', 'E_Cylinder', 'F_Sphere', 'G_Monkey'],
            'map': lambda x: x.lower(),
            'val': lambda x: True if x.lower() in ["on", "off"] else False
        },
        {
            'ids': ["topradius", "topr"],
            'type': ['E_Cylinder'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["killer", "k"],
            'type': ['B_Platform', 'E_Cylinder', 'F_Sphere'],
            'map': lambda x: x.lower(),
            'val': lambda x: True if x.lower() in ["on", "off"] else False
        },
        {
            'ids': ["movementx", "mx"],
            'type': ['B_Platform', 'E_Cylinder', 'C_Cone', 'D_End', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["movementy", "my"],
            'type': ['B_Platform', 'E_Cylinder', 'C_Cone', 'D_End', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["movementz", "mz"],
            'type': ['B_Platform', 'E_Cylinder', 'C_Cone', 'D_End', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["rotationx", "rx"],
            'type': ['B_Platform', 'E_Cylinder', 'C_Cone', 'D_End', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["rotationy", "ry"],
            'type': ['B_Platform', 'E_Cylinder', 'C_Cone', 'D_End', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["rotationz", "rz"],
            'type': ['B_Platform', 'E_Cylinder', 'C_Cone', 'D_End', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["bounce", "bou"],
            'type': ['B_Platform', 'E_Cylinder', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["mass", "mass"],
            'type': ['B_Platform', 'E_Cylinder', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["friction", "fr"],
            'type': ['B_Platform', 'E_Cylinder', 'F_Sphere', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["brightness", "br"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["background", "bg"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': hex_map,
            'val': hex_val
        },
        {
            'ids': ["ambientColor", "amb"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': hex_map,
            'val': hex_val
        },
        {
            'ids': ["diffuseColor", "dif"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': hex_map,
            'val': hex_val
        },
        {
            'ids': ["specularColor", "spe"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': hex_map,
            'val': hex_val
        },
        {
            'ids': ["groundColor", "gro"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': hex_map,
            'val': hex_val
        },
        {
            'ids': ["cameraDistance", "d"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': positive_val
        },
        {
            'ids': ["cameraEyesight", "eye"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': positive_val
        },
        {
            'ids': ["cameraDownAngle", "cd"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': lambda x: True if -60 < int(x) < 60 else False
        },
        {
            'ids': ["cameraRightAngle", "cr"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["cameraRightAngle", "cr"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["cameraRightAngle", "cr"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["cameraRightAngle", "cr"],
            'type': ['A_Section', 'G_Monkey', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["setRotation", "sr"],
            'type': ['A_Section', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["use"],
            'type': ['A_Section', 'B_Platform', 'E_Cylinder', 'C_Cone', 'D_End', 'F_Sphere', 'G_Monkey', 'G_Monkey'],
            'map': lambda x: str(x),
            'val': use_name_val
        },
        {
            'ids': ["jump", "j", "jump"],
            'type': ['B_Platform', 'G_Monkey'],
            'map': lambda x: x.lower(),
            'val': lambda x: True if x.lower() in ["on", "off"] else False
        },
        {
            'ids': ["drift", "dr"],
            'type': ['B_Platform', 'G_Monkey'],
            'map': lambda x: x.lower(),
            'val': lambda x: True if x.lower() in ["on", "off"] else False
        },
        {
            'ids': ["jumpSpeed", "js"],
            'type': ['A_Section', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        },
        {
            'ids': ["jumpHeight", "jh"],
            'type': ['A_Section', 'G_Monkey'],
            'map': decimal_map,
            'val': decimal_val
        }
    ]
 
    def eff_process(x, item, accum):
        equal_split = x.strip().split("=")
        if len(equal_split) == 1:
            return [];
        equal_left = str(equal_split[0].strip())
        equal_right = equal_split[1].strip()
 
        key = equal_left
 
        if key in deprecation_mapping:
            return [{
                'err': "Deprecation notice: " + deprecation_mapping[key]
            }] + accum;
 
        effect_found = False
        effect_index = -1;
        for effect in effects:
            effect_index += 1;
            if key.lower() in list(map(lambda x: x.lower(), effect['ids'])):
                effect_found = True
                break;
 
        effect = effects[effect_index] if effect_found == True else None
 
        if effect == None:
            return [{
                'err': "There is no such effector as '" + key + "'"
            }] + accum;
 
 
        if effect['val'](equal_right) == False:
            return [{
                'err': "Effector '" + key + "' can not have value '" + equal_right + "'"
            }] + accum;
 
        if effect['ids'][0] == "use" and item['type'] != "G_Monkey":
            import_monkeys = []
            for use_ar in use_arr:
                for efff in use_ar:
                    check_match = "use="+equal_right
                    if efff == check_match:
                        use_ar.remove(check_match)
                        print(use_ar)
                        import_monkeys = import_monkeys + use_ar
            return import_monkeys + accum
 
        if item['type'] not in effect['type']:
            return [{
                'err': "Effector '" + key + "' is not compatible with this object type. ("+item['type']+")"
            }] + accum;
 
        val = str(effect['map'](equal_right))
        alias = effect['ids'][1] if len(effect['ids']) == 2 else effect['ids'][0]
        return [alias+"="+val] + accum
 
 
    def item_to_eff(item):
        global use_index;
        try:
            between_brackets = ""
            msg_mode = False
            eff_mode = False
            for char in item['name']:
                if char == "{" and eff_mode == True and msg_mode == False:
                    msg_mode = True
                elif char == "}" and eff_mode == True and msg_mode == True:
                    msg_mode = False
                elif char == "[" and eff_mode == False and msg_mode == False:
                    eff_mode = True
                elif char == "]" and eff_mode == True and msg_mode == False:
                    eff_mode = False
                    between_brackets += ","
                else:
                    if eff_mode == True:
                        if msg_mode == False:
                            between_brackets += char;
                        elif msg_mode == True:
                            between_brackets += str(ord(char))+":";
 
            comma_split = between_brackets.split(",")
            res = []
            is_use = False
            is_donut = False
            for x in comma_split:
                for ef in eff_process(x, item, []):
                    if 'err' in ef:
                        return ef;
                    res.append(ef)
                    if item['type'] == "G_Monkey":
                        use_arr[use_index].append(ef)
                        if "use=" in ef:
                            is_use = True
 
            if is_use == True:
                use_index += 1
                return "";
            else:
                return "?".join(res)
        except Exception as e:
            print(str(e))
            return {
                'err': "Please double check that the name is correctly formatted."
            }
 
    for item in items:
        if item['err'] == []:
            eff = item_to_eff(item)
            if 'err' in eff:
                item['err'].append(eff['err'])
            else:
                if item['type'] in ["G_Monkey", "I_Donut"]:
                    item['eff'] = eff
 
    for item in items:
        if item['err'] == []:
            eff = item_to_eff(item)
            if 'err' in eff:
                item['err'].append(eff['err'])
            else:
                if item['type'] not in ["G_Monkey", "I_Donut"]:
                    if "[" in item['name'] and "]" in item['name']:
                        item['eff'] = eff                
 
 
    ### FATAL ERROR CHECK
    # item count
    fatal_errors = []
    if len(items) > 100:
        print("Warning: You have " + str(len(items)) + " / 300 objects in this map.")
    elif len(items) > 300:
        fatal_errors.append("There are too many items in this map. " + str(len(items)) + " > 300")
 
    # item errors
    for item in items:
        if item['err'] != []:
            fatal_errors.append("For item '" + str(item['name']) + "': " + str(item['err']))
 
    # plane
    if len(fatal_errors) == 0:
        section_list = []
        for item in items:
            if item['type'] == "A_Section":
                loc = item['obj'].location[1]
                sca = item['obj'].scale[1]
                section_list.append([loc, sca])
 
        section_list = list(reversed(sorted(section_list, key=lambda x: x[0])))
        if len(section_list) > 0:
            # behind spawn
            if section_list[0][0] + abs(section_list[0][1]) > 0:
                fatal_errors.append("Planes can not extend behind the spawnpoint.")
 
            # overlaps
            # if len(fatal_errors) == 0:
            #     for i in range(len(section_list) - 1):
            #         s1 = section_list[i]
            #         s2 = section_list[i+1]
            #         a1 = abs(float(s1[0])) + abs(float(s1[1]))
            #         a2 = abs(float(s2[0])) - abs(float(s2[1]))
            #         if (a2 < a1):
            #             fatal_errors.append("Overlapping planes are not permitted.")
            #             break;
 
    # ending count
    if len(fatal_errors) == 0:
        ending_count = 0
        for item in items:
            if item['type'] == "D_End":
                ending_count += 1
 
        if ending_count == 0:
            fatal_errors.append("Please add an ending. Add > Mesh > UV Sphere")
 
 
    # ID match
    if len(fatal_errors) == 0:
        section_ids = []
        solid_ids = []
        for item in items:
            if "id=" in item['eff']:
                id_split = item['eff'].split("id=")[1]
                obj_id = id_split.split("?")[0] if "?" in id_split else id_split.split("]")[0]
                if item['type'] == "A_Section":
                    section_ids.append(obj_id)
                elif item['type'] in ['B_Platform', 'C_Cone', 'D_End', 'E_Cylinder', 'F_Sphere']:
                    solid_ids.append(obj_id)
 
    # Opacity requires Material
    if len(fatal_errors) == 0:
        for item in items:
            if "o=" in item['eff'] and "gro=" not in item['eff']:
                spl = item['eff'].split("m=")
                if len(spl) != 2 or len(spl[1].split(",")[0]) < 6:
                    fatal_errors.append("Opacity requires HEX material. Item name = " + str(item['name']));
 
    if len(fatal_errors) > 0:
        print("")
        print("FATAL ERRORS:")
        for fatal_error in fatal_errors:
            print("- " + str(fatal_error))
        print("")
    else:
        # URL = "http://localhost:5000/?mapCodeVersion=v8&mapUrl="
        URL = "https://onionfist.com/icedodo/?mapCodeVersion=v8&mapUrl="
 
        for item in items:
            URL += item['type'][0] + "$".join(list(map(str, item['pos'] + item['rot'] + item['siz']))) + "$" + item['eff']
 
        # URL SHORTENER
        shortURL = ""
        foundDot = False
        for i, character in enumerate(URL):
            if character == ".":
                foundDot = True
                startPos = i
                endPos = i
            elif foundDot:
                if character.isnumeric():
                    endPos += 1
                else:
                    foundDot = False
                    # analyse number
                    number = URL[startPos:endPos+1]
                    if (
                        number == ".007" or
                        number == ".014" or
                        number == ".021" or
                        number == ".028" or
                        number == ".035" or
                        number == ".042" or
                        number == ".049"
                    ):
                        # do nothing (don't append number)
                        pass
                    elif (
                        number == ".951" or
                        number == ".958" or
                        number == ".965" or
                        number == ".972" or
                        number == ".979" or
                        number == ".986" or
                        number == ".993"
                    ):
                        j = startPos-1
                        end = j
                        start = j+1
                        while True:
                            if URL[j].isnumeric():
                                start -= 1
                            else:
                                break
                            j-=1          
 
                        sublength = len(URL[start:end+1])            
                        shortURL = shortURL[:-sublength]
                        shortURL += str(int(URL[start:end+1]) + 1)
                    else:
                        shortURL += URL[startPos:endPos+1]
                    shortURL += character
            else:
                shortURL += character
 
        print(f"Characters before shortening: {len(URL)}")
        print(f"Characters after shortening: {len(shortURL)}")
 
        if len(shortURL) > 8938:
            print("Warning: URL Length exceeds 8938 characters. This may or may not cause an issue.")
 
        print("")
        print("MAP URL:")
        print("")
        print(shortURL)
        print("")
 
except Exception as main_e:
    print("MAIN ERROR: " + str(main_e))
 
##############################################
# COPY AND PASTE UNTIL HERE (including this) #
##############################################