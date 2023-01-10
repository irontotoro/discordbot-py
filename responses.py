import random


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == '안녕':
        return '안녕 난 재웅이야'
        
    if p_message == '재웅아 뭐해':
        return '재웅이는 김장해'

    if p_message == '재웅아 노래 추천해줘':
        return 'https://www.youtube.com/watch?v=4_589PAbssI'

    if message == '재웅아 민증몇개야':
        return str(random.randint(2, 10))

    if p_message == '재웅이가 누구야?':
        return '`\n이름:이재웅\n나이:20\n출생지:베트남\n학력:한가람고 재학중`'
    
    if p_message == '!help':
        return '`외국인 재웅이는 아쉽게도 도움을 줄 수 없어요`'

    
