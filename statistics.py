import dao
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.font_manager as fm
from config import PLATFORM, MACOS

matplotlib.use('TkAgg')
# 设置中文字体
zh_font = fm.FontProperties(fname='/System/Library/Fonts/PingFang.ttc') if PLATFORM == MACOS \
    else fm.FontProperties(fname='C:\\Windows\\Fonts\\SimHei.ttf')


def gen_bar_chart(categories, values, title, x_label, y_label):
    bars = plt.bar(categories, values, color='skyblue')
    plt.title(title, fontproperties=zh_font)
    plt.xlabel(x_label, fontproperties=zh_font)
    plt.ylabel(y_label, fontproperties=zh_font)
    plt.savefig('chart/bar_chart.png')
    # 倾斜 x 轴标签
    plt.xticks(rotation=45)
    # 在每个条形的顶部显示具体数值
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')
    # 调整图形的边距
    plt.subplots_adjust(bottom=0.2)
    plt.show()


def gen_pie_chart(labels, sizes, title):
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontproperties': zh_font})
    plt.axis('equal')
    plt.title(title, fontproperties=zh_font)
    plt.savefig('chart/pie_chart.png')
    plt.show()


def get_past_dates(n):
    today = datetime.today()
    date_list = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(n, -1, -1)]
    return date_list


def gen_chart_with_subplots(bar_chart_categories, bar_chart_values, bar_chart_title, bar_chart_x_label, bar_chart_y_label,
                            pie_chart_1_labels, pie_chart_1_sizes, pie_chart_1_title,
                            pie_chart_2_labels, pie_chart_2_sizes, pie_chart_2_title):
    # 创建2x2的子图布局，即4个子图
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    # 第一个子图：条形图
    bars = axs[0, 0].bar(bar_chart_categories, bar_chart_values, color='skyblue')
    axs[0, 0].set_title(bar_chart_title, fontproperties=zh_font)
    axs[0, 0].set_xlabel(bar_chart_x_label, fontproperties=zh_font)
    axs[0, 0].set_ylabel(bar_chart_y_label, fontproperties=zh_font)
    # 倾斜 x 轴标签
    axs[0, 0].tick_params(axis='x', rotation=45)
    # 在每个条形的顶部显示具体数值
    for bar in bars:
        height = bar.get_height()
        axs[0, 0].text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')

    # 第二个子图：饼状图
    axs[0, 1].pie(pie_chart_1_sizes, labels=pie_chart_1_labels, autopct='%1.1f%%', startangle=140,  textprops={'fontproperties': zh_font})
    axs[0, 1].set_title(pie_chart_1_title, fontproperties=zh_font)

    # 第三个子图：饼状图
    axs[1, 0].pie(pie_chart_2_sizes, labels=pie_chart_2_labels, autopct='%1.1f%%', startangle=140,  textprops={'fontproperties': zh_font})
    axs[1, 0].set_title(pie_chart_2_title, fontproperties=zh_font)

    # 自动调整子图参数，使得布局紧凑
    # plt.tight_layout()

    # 调整子图之间的垂直间距
    plt.subplots_adjust(hspace=0.7)  # 这里设置间距为0.7，可以根据需要调整

    # 显示图形
    plt.show()


def main():
    # 统计近7天每天的按键数量
    date_count = dao.get_count_group_by_date()
    date_count_map = {} if date_count is None or len(date_count) == 0 else {dc['date']: dc['count'] for dc in date_count}
    # 生成最近7天的日期，格式为"yyyy-MM-dd"
    date_list = get_past_dates(6)
    date_count_list = [date_count_map.get(date, 0) for date in date_list]

    # 统计最近7天按键数量最多的10个按键分别按了多少次
    key_count = dao.get_count_group_by_key()
    key_list = [] if key_count is None or len(key_count) == 0 else [kc['key_show_name'] for kc in key_count]
    count_list = [] if key_count is None or len(key_count) == 0 else [kc['count'] for kc in key_count]

    # 统计最近7天的正确率
    right_count, error_count = dao.get_right_and_error_count()
    labels = ['正确', '错误']
    sizes = [right_count, error_count]

    gen_chart_with_subplots(date_list, date_count_list, '最近7天按键数量', '日期', '按键数量',
                            key_list, count_list, 'Top5按键数量占比',
                            labels, sizes, '最近7天正确率')


if __name__ == '__main__':
    main()
