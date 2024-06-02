from config import db_client as db


def save_record(record):
    sql = "INSERT INTO keyboard_press_record " \
          "(key_show_name, key_name, key_vk, press_time, platform) VALUES (%s, %s, %s, %s, %s)"
    db.db_execute(sql, record.key_show_name, record.key_name, record.key_vk, record.press_time, record.platform)


def get_count_group_by_date():
    """
    获取最近7天每天的按键数量
    :return:
    """
    sql = """
        SELECT
            DATE_FORMAT(press_time, '%Y-%m-%d') AS `date`,
            COUNT(*) AS `count`
        FROM `keyboard_record`.`keyboard_press_record`
        WHERE press_time >= CURDATE() - INTERVAL 7 DAY
        GROUP BY DATE_FORMAT(press_time, '%Y-%m-%d')
        order by `date`;
    """
    return db.query_all(sql)


def get_count_group_by_key():
    """
    获取最近几天每个按键的按键数量
    :param date: 字符串，格式为"yyyy-MM-dd"
    :return:
    """
    sql = """
        -- 获取前10个按键及其次数
        WITH TopKeys AS (
            SELECT key_show_name, COUNT(*) AS count
            FROM keyboard_record.keyboard_press_record
            WHERE press_time >= CURDATE() - INTERVAL 7 DAY
            GROUP BY key_show_name
            ORDER BY count DESC
            LIMIT 5
        ),
        -- 获取除了前10个按键外的其他按键的总和
        OtherKeys AS (
            SELECT '其他' AS key_show_name, SUM(count) AS count
            FROM (
                SELECT key_show_name, COUNT(*) AS count
                FROM keyboard_record.keyboard_press_record
                WHERE press_time >= CURDATE() - INTERVAL 7 DAY
                GROUP BY key_show_name
                ORDER BY count DESC
                LIMIT 5, 18446744073709551615 -- 18446744073709551615 是 MySQL 中的最大 UNSIGNED BIG INT 值，用于表示无穷大
            ) AS subquery
        )

        -- 将前10个按键和其他按键的总和合并
        SELECT * FROM TopKeys
        UNION ALL
        SELECT * FROM OtherKeys;
    """
    return db.query_all(sql)


def get_right_and_error_count():
    # 获取最近7天的按键总数
    sql1 = "select count(*) from keyboard_press_record where press_time >= CURDATE() - INTERVAL 7 DAY"
    # 获取最近7天的退格键按键总数
    sql2 = "select count(*) from keyboard_press_record where press_time >= CURDATE() - INTERVAL 7 DAY and key_show_name = 'Backspace'"
    total_count = db.query_count(sql1)
    backspace_count = db.query_count(sql2)
    return total_count - backspace_count * 2, backspace_count