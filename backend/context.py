from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DESCRIPTION = [
"""
Программные роботы «Атом.РИТА» автоматизируют рутинные задачи в бухгалтерии, управлении персоналом и финансах. 
Задачи включают оформление отчетов, акты сверки, авансовые отчеты, создание графиков отпусков и контроль заявок на оплату.
Преимущества: поддержка пользователей, облачная архитектура, шифрование данных, low-code инструменты, снижение затрат, выполнение KPI.
""",
"""
Система «Логос» — решение для математического моделирования и инженерного анализа в промышленных задачах. 
Преимущества: отечественная разработка, высокая точность, проект импортозамещения CAE, интеграция с российскими CAD/CAE-системами.
""",
"""
«Сарус» — система управления предприятиями с модулями для управления производством, персоналом и жизненным циклом изделий. 
Преимущества: импортонезависимость, соответствие требованиям безопасности, обработка данных до уровня «Совершенно секретно», применение в КИИ.
"""
]

def find_similar_texts(question):
    """
    Find similar texts based on TF-IDF and cosine similarity.

    Args:
        question (str): The question to find similar texts for.
        texts (List[str]): A list of texts to search in.

    Returns:
        str: The most similar text.
    """
    question_lower = question.lower()

    keywords = {
        "атом.рита": 0,
        "логос": 1,
        "сарус": 2
    }

    for keyword, index in keywords.items():
        if keyword.lower() in question_lower:
            return DESCRIPTION[index]

    return ""

def remove_non_printable(s):
    return ''.join(c for c in s if c.isprintable())