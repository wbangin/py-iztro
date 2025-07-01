from py_iztro import Astro

import json
import argparse

def format_star(star: dict) -> str:
    """将单个星耀对象格式化为可读字符串。"""
    name = star.get('name', '')
    brightness = star.get('brightness', '')
    mutagen = star.get('mutagen', '')
    
    parts = [name]
    details = []
    if brightness:
        details.append(brightness)
    # 确保四化不为空字符串
    if mutagen and mutagen.strip():
        details.append(mutagen)
        
    if details:
        parts.append(f"({', '.join(details)})")
        
    return "".join(parts)

def print_ziwei_chart(data: dict):
    """以人类可读的格式打印紫微斗数命盘。"""
    
    print("*** 个人基本信息 ***")
    print(f"性别: {data.get('gender')}")
    print(f"阳历: {data.get('solarDate')}")
    print(f"阴历: {data.get('lunarDate')}")
    print(f"四柱: {data.get('chineseDate')}")
    print(f"时辰: {data.get('time')} ({data.get('timeRange')})")
    print(f"星座: {data.get('sign')}")
    print(f"生肖: {data.get('zodiac')}")
    print("*" * 20)
    print(f"命主: {data.get('soul')}")
    print(f"身主: {data.get('body')}")
    print(f"五行局: {data.get('fiveElementsClass')}")
    print(f"身宫地支: {data.get('earthlyBranchOfBodyPalace')}")
    print(f"命宫地支: {data.get('earthlyBranchOfSoulPalace')}")
    print("\n" + "="*10 + " 十二宫位详情 " + "="*10)

    palaces = data.get('palaces', [])
    # 按宫位索引排序，确保顺序正确
    palaces.sort(key=lambda p: p.get('index', 0))

    for palace in palaces:
        palace_name = palace.get('name', '未知宫位')
        heavenly_stem = palace.get('heavenlyStem', '?')
        earthly_branch = palace.get('earthlyBranch', '?')
        
        print(f"\n *** {palace_name}宫 (天干: {heavenly_stem}, 地支: {earthly_branch}):")

        if palace.get('isBodyPalace'):
            print("  [身宫]")
        if palace.get('isOriginalPalace'):
            print("  [原始宫位]")

        major_stars = [format_star(s) for s in palace.get('majorStars', [])]
        if major_stars:
            print(f"  主星: {', '.join(major_stars)}")

        minor_stars = [format_star(s) for s in palace.get('minorStars', [])]
        if minor_stars:
            print(f"  辅星/煞星: {', '.join(minor_stars)}")

        adjective_stars = [format_star(s) for s in palace.get('adjectiveStars', [])]
        if adjective_stars:
            print(f"  杂曜: {', '.join(adjective_stars)}")
            
        #print("-" * 15)
        print(f"  长生十二神: {palace.get('changsheng12')}")
        print(f"  博士十二神: {palace.get('boshi12')}")
        print(f"  岁前十二神: {palace.get('suiqian12')}")
        print(f"  将前十二神: {palace.get('jiangqian12')}")

        decadal = palace.get('decadal', {})
        decadal_range = decadal.get('range', [])
        if decadal_range:
            print(f"  大限: {decadal_range[0]}-{decadal_range[1]}岁")
            
        ages = palace.get('ages', [])
        if ages:
            print(f"  流年: {', '.join(map(str, ages))}")
        print("*" * 3)

def main():
    parser = argparse.ArgumentParser(
        description="根据公历生日和时间排紫微斗数命盘，并以易读格式输出。",
        epilog="""使用示例:
  python iztra.py "2000-02-02 09:30" 男
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "datetime",
        help="出生日期和时间，格式为 'YYYY-MM-DD HH:MM' (建议用引号括起来)"
    )
    parser.add_argument(
        "gender",
        choices=['男', '女'],
        help="性别 ('男' 或 '女')"
    )

    args = parser.parse_args()



    try:
        # 从参数中解析日期和小时
        date_part, time_part = args.datetime.split()
        hour = int(time_part.split(':')[0])
        time_index=(hour-1)//2 + 1
    except ValueError:
        print("错误：日期时间格式不正确。请确保格式为 'YYYY-MM-DD HH:MM'。")
        return
    print("【排盘输入信息】")
    print(f"  公历时间: {args.datetime}")
    print(f"  性别: {args.gender}")
    print(f"  时辰: {time_index}")
    print("-" * 25, "\n")
    astro = Astro()
    # 使用从命令行获取的参数进行排盘
    result = astro.by_solar(date_part, time_index, args.gender)
    #print(result.model_dump_json(by_alias=True, indent=4))
    ziwei_data = result.model_dump(by_alias=True)
    print_ziwei_chart(ziwei_data)

if __name__ == '__main__':
    main()
