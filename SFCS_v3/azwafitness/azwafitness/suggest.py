def suggest():
    result_Suggest = []
    list_tong = ['type_Body_list', 'age_range_list', 'gender_list', 'goal_list', 'physical_Condition_list']
    for item in list_tong:
        print("item:", item)
        if item == 'type_Body':
            for val in type_Body_list:
                print("val:", val)
                if val == "Extremely Weak":
                    result_Suggest.append("a")
                elif val == "Weak":
                    result_Suggest.append("b")
                elif val == "Normal":
                    result_Suggest.append("c")
                elif val == "Overweight":
                    result_Suggest.append("d")
                elif val == "Obesity":
                    result_Suggest.append("e")
                elif val == "Extreme Obesity":
                    result_Suggest.append("f")
        elif item == 'age_range':
            for val in age_range_list:
                print("val:", val)
                if val == '0':
                    result_Suggest.append("1") 
                elif val == '1':
                    result_Suggest.append("2")
                elif val == '2':
                    result_Suggest.append("3")
                elif val == '3':
                    result_Suggest.append("4")
        elif item == 'gender':
            for val in gender_list:
                print("val:", val)
                if val == 1.0:
                    result_Suggest.append("A") 
                elif val == 0.0:
                    result_Suggest.append("B")
        elif item == 'goal':
            for val in goal_list:
                print("val:", val)
                if val == "lose_weight":
                    result_Suggest.append("I") 
                elif val == "gain_muscle_mass":
                    result_Suggest.append("II")
                elif val == "get_shredded":
                    result_Suggest.append("III")
        elif item == 'physical_Condition':
            for val in physical_Condition_list:
                print("val:", val)
                if val == 'ectomorph':
                    result_Suggest.append("q") 
                elif val == 'mesomorph':
                    result_Suggest.append("w")
                elif val == 'endomorph':
                    result_Suggest.append("e")
        else:
            result_Suggest.append("This is an exception")
    return result_Suggest
