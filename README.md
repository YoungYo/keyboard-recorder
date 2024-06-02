# keyboard-recorder
一个记录键盘敲击记录的小工具

# 配置文件
需要在项目根目录下创建一个配置文件，文件名为`config.json`，配置项如下：
```json
{
  "datasource": {
    "host": "localhost",
    "port": 3306,
    "user": "username",
    "password": "password",
    "database": "test"
  }
}
```
下面对配置项进行解释：
- `datasource`：数据源配置
  - `host`：数据库主机地址
  - `port`：数据库端口
  - `database`：数据库名称
    
如果配置了数据源，需要在数据库中创建一个表，表结构如下：
```sql
CREATE TABLE `keyboard_record`.`keyboard_press_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT comment '主键ID',
  `key_show_name` varchar(255) DEFAULT NULL comment '按键的外显名称',
  `key_name` varchar(255) default null comment '按键的实际名称',
  `key_vk` int default null comment '按键的值',
  `press_time` datetime DEFAULT NULL comment '敲击时间',
  `platform` varchar(255) default null comment '操作系统',
  `create_time` datetime default current_timestamp comment '当前记录的创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```