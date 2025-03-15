
def sign_upup(num, user_list, id, password):
    global overlap
    overlap = False

    for i in range(num): 
        if id == user_list[i][0]:
            overlap = True
            result = id+"는(은) 이미 존재하는 id입니다. 다시 입력해주세요."
            return result

    if not(overlap): 
        if " " in id or " " in password:
            result = "아이디와 비밀번호에는 공백이 포함될 수 없습니다."
            
            return result
        
        else:
            result = "계정이 생성되었습니다."
        
            with open("user_file.txt", 'a') as file: 
                file.write(id + " " + password+"\n") 
            
            return result
    



def loginin(num, user_list, id, password):
    global overlap
    overlap = False

    for i in range(num):
        if id == user_list[i][0] and password == user_list[i][1]:
            result = "로그인에 성공하셨습니다.\n"+id+"님 환영합니다."
            overlap = True

            return result
        

    if not(overlap):
        global overlap2
        overlap2 = False
        
        for i in range(num):
            if id == user_list[i][0]:
                overlap2 = True
                break

        if not(overlap2):
            result = "존재하지 않는 아이디입니다. 다시 입력해주세요."

            return result
            
        if overlap2 == True:
            global overlap3
            overlap3 = False

            for i in range(num):
                if password == user_list[i][1]:
                    overlap3 = True

                    break

            if not(overlap3):
                result = "비밀번호가 틀렸습니다. 다시 입력해주세요."

                return result



def deldel_user(num, user_list, id, password):
    global overlap
    overlap = False

    global idx
    idx = None

    for i in range(num):
        if id == user_list[i][0] and password == user_list[i][1]:
            result = id+"의 계정이 삭제되었습니다."
            overlap = True 
            

            for i in range(num):
                if id == user_list[i][0]:
                    idx = i
                    break

            del user_list[idx]
            num = len(user_list)

            for i in range(num):
                user_list[i] = " ".join(user_list[i])

            user_list = "\n".join(user_list)

            with open ("user_file.txt", "w") as file:
                file.write(user_list)

            return result

    if not(overlap):
        global overlap2
        overlap2 = False

        for i in range(num):
            if id == user_list[i][0]:
                overlap2 = True
                break

        if not(overlap2):
            result = id+"는(은) 존재하지 않는 아이디입니다. 다시 입력해주세요."

            return result

        if overlap2 == True:
            global overlap3
            overlap3 = False

            for i in range(num):
                if password == user_list[i][1]:
                    overlap3 = True
                    break

            if not(overlap3):
                result = "비밀번호가 틀렸습니다. 다시 입력해주세요."

                return result

