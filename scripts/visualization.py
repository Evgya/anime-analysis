import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud


def plot_donut_chart(df, column):
    """
    Строит пончиковую диаграмму для отображения пропущенных и заполненных значений в указанном столбце DataFrame.

    Параметры:
        df (pandas.DataFrame): DataFrame, содержащий данные.
        column (str): Название столбца, для которого строится диаграмма.

    Возвращает:
        None: Функция отображает диаграмму, но не возвращает значений.
    """
    missing_values = df[column].isna()

    missing_count = missing_values.sum()
    filled_count = len(df) - missing_count

    sizes = [missing_count, filled_count]
    labels = ['Пропуски', 'Заполненные значения']
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.3),
        autopct=lambda p: '{:.0f}%\n({:.0f})'.format(p, (p/100)*sum(sizes)),
        pctdistance=0.85,
        shadow=True        
    )
    ax.set_xlim(-2.5, 1)
    ax.set_title(column, x=0.715)   

    plt.show()
    
 
def plot_bar(column, title='', limit=10):
    """
    Создает столбчатую диаграмму на основе данных из указанного столбца.

    Параметры:
    ----------
    column : pd.Series
        Столбец, содержащий данные, по которым будет строиться диаграмма. Значения в столбце должны быть категориальными.

    title : str, optional
        Заголовок диаграммы (по умолчанию пустая строка).

    xlabel : str, optional
        Подпись для оси X (по умолчанию пустая строка).

    ylabel : str, optional
        Подпись для оси Y (по умолчанию пустая строка).

    Описание:
    ---------
    Функция подсчитывает количество вхождений каждого уникального значения в столбце, сортирует их в порядке убывания и
    строит столбчатую диаграмму с этими данными. Каждый столбец диаграммы окрашен в оттенок синего, где более насыщенные 
    цвета соответствуют более высоким значениям. Над каждым столбцом отображается процентное соотношение данного значения 
    от общего числа. Дополнительно скрываются некоторые элементы диаграммы для улучшения визуального восприятия.

    """
    type_counts = column.value_counts().sort_values(ascending=False)
    
    top_categories = type_counts.head(limit)
    
    if len(type_counts) > limit:
        # Объединение остальных категорий в 'Other'
        other_count = type_counts[limit:].sum()
        top_categories['Other'] = other_count   
    

    sns.barplot(
        x=top_categories.index, y=top_categories, 
        palette=sns.color_palette("Blues", len(top_categories))[::-1], 
        order=top_categories.index
    )
    

    top_categories_sum = top_categories.sum()
    for index, value in enumerate(top_categories):
        plt.text(index, value + 0.5, f'{(value/top_categories_sum)*100:.0f}%', ha='center', va='bottom')

    plt.title(title)
    plt.xticks(rotation=45)   
    plt.ylim(0, max(top_categories) + 40)
    
    plt.gca().axes.yaxis.set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_linewidth(1)

    plt.show()


def plot_horizontal_bar(column, title='', limit=10):
    """
    Создает горизонтальную столбчатую диаграмму для визуализации распределения категорий в столбце с возможностью ограничения 
    количества отображаемых категорий и объединением остальных в категорию 'Other'.

    Параметры:
    ----------
    column : pd.Series
        Столбец с категориальными данными, по которым будет строиться диаграмма.
    
    title : str, optional
        Заголовок диаграммы (по умолчанию пустая строка).
    
    limit : int, optional
        Количество наиболее частых категорий, которые будут отображены на диаграмме. Остальные категории будут объединены 
        в 'Other' (по умолчанию 10).
    
    Описание:
    ---------
    Функция подсчитывает количество вхождений для каждого уникального значения в столбце, сортирует их по убыванию и выделяет 
    наиболее частые категории в соответствии с параметром 'limit'. Если количество уникальных категорий больше указанного 
    лимита, остальные объединяются в категорию 'Other'. Для каждой категории на диаграмме отображается процентное соотношение 
    относительно общего числа вхождений. Также скрываются оси и некоторые элементы диаграммы для улучшения визуального восприятия.

    Пример:
    -------
    >>> plot_horizontal_bar(df['Genres'], title='Top 10 Genres', limit=10)
    
    Это построит горизонтальную столбчатую диаграмму с топ-10 наиболее часто встречающимися категориями в столбце 'Genres' 
    и объединит остальные в 'Other'.
    """
    
    type_counts = column.value_counts().sort_values(ascending=False)
    
   
    top_categories = type_counts.head(limit)
    
    if len(type_counts) > limit:
        # Объединение остальных категорий в 'Other'
        other_count = type_counts[limit:].sum()
        top_categories['Other'] = other_count   
    
    
    sns.barplot(
        y=top_categories.index, x=top_categories, 
        palette=sns.color_palette("Blues", len(top_categories))[::-1], 
        order=top_categories.index
    )
    
    
    total_sum = top_categories.sum()
    for index, value in enumerate(top_categories):
        plt.text(value + 0.5, index, f'{(value/total_sum)*100:.0f}%', ha='left', va='center')
    
    
    plt.title(title)
    plt.xlim(0, max(top_categories) + 40)
    plt.gca().axes.xaxis.set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_linewidth(1)
    plt.gca().spines['bottom'].set_visible(False)
    
    plt.show()
    
 
def plot_correlation_matrix(data, title=''):
    """
    Визуализирует тепловую карту корреляционной матрицы для числовых данных из переданного DataFrame.

    Параметры:
    ----------
    data : pandas.DataFrame
        Набор данных, содержащий числовые столбцы, для которых будет вычислена и визуализирована корреляционная матрица.
        
    title : str, optional, default=''
        Заголовок графика. Если передан, отображается вверху графика.

    Возвращаемое значение:
    ----------------------
    None
        Функция не возвращает значение, а выводит график на экран.

    Пример:
    -------
    >>> data = pd.DataFrame({
    ...     'A': [1, 2, 3, 4, 5],
    ...     'B': [5, 4, 3, 2, 1],
    ...     'C': [2, 3, 4, 5, 6]
    ... })
    >>> plot_correlation_matrix(data, title='Корреляционная матрица')
    """
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='Blues', fmt=".2f", linewidths=.5)
    plt.title(title)
    plt.show()
 
 
def plot_word_cloud(series, title=''):
    """
    Построение облака слов (Word Cloud) на основе частотного распределения в pandas.Series.

    Параметры:
    ----------
    series : pandas.Series
        Серия данных, содержащая слова или категории.
    
    title : str, optional
        Заголовок для графика (по умолчанию пустая строка).
    
    Возвращает:
    -----------
    None
        Функция строит и отображает облако слов с использованием частот, вычисленных из 'series'.
    """
    
    frequencies = series.value_counts()

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()