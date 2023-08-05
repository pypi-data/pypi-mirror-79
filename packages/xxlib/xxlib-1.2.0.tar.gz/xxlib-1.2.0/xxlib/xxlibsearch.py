# -*- coding:utf-8 -*-



#-----------------------------------------------#
#                  搜索引擎库                    #
#-----------------------------------------------#
#             作者：轩轩    轩轩工作室            #
#-----------------------------------------------#
#               版权所有，翻版必究                #
#-----------------------------------------------#
#               商业使用请联系作者                #
#-----------------------------------------------#
#          该代码未开源，如果你看到代码...         #
#                  希望你能懂                    #
#-----------------------------------------------#
#               该库仍在更新中                   #
#-----------------------------------------------#











import webbrowser

def internet(name):
    webbrowser.open(name)

def baidu(name):  # 百度
    webbrowser.open("https://www.baidu.com/s?wd=" + name)


def so(name):  # 360
    webbrowser.open("https://www.so.com/s?ie=utf-8&src=360se7_addr&q=" + name)


def sogo(name):  # 搜狗浏览器
    webbrowser.open("https://www.sogou.com/web?query=" + name)


def bycn(name):  # 必应国内
    webbrowser.open("https://cn.bing.com/search?q=" + name)


def MBA(name):  # MBA智库
    webbrowser.open("https://www.mbalib.com/s?q=" + name)


def aiqiyi(name):  # 爱奇艺搜索
    webbrowser.open("http://so.iqiyi.com/so/q_" + name)


def sole(name):  # 搜了网
    webbrowser.open("http://s.51sole.com/s.aspx?q=" + name)


def weibo(name):  # 微博搜索
    webbrowser.open("https://s.weibo.com/weibo?q=" + name)


def cnso(name):  # 中国搜索
    webbrowser.open("http://www.chinaso.com/search/pagesearch.htm?q=" + name)


def taobao(name):  # 淘宝搜索
    webbrowser.open("https://s.taobao.com/search?initiative_id=staobaoz_20200824&q=" + name)


def ty(name):  # 统一搜索
    webbrowser.open("http://stock1.com.cn/plus/search.php?kwtype=" + name)


def easou(name):  # 宜搜搜索
    webbrowser.open("http://i.appeasou.com/s.m?idx=1&sty=1&q=" + name)


def xxso(name):
 if name=="陈逸轩":
        print("该库开发者，还开发手机APP")

 if name == "学而思网校":
        print("学而思网校，为6-18岁孩子提供小初高全学科课外教学，纽交所上市公司旗下品牌。十余年教学沉淀，“直播+辅导”双师模式，AI技术辅助教学。全国200多个城市的中小学生都在网校学习。")

 if name == "钉钉":
     print(
        "钉钉（DingTalk）是阿里巴巴集团专为中国企业打造的免费沟通和协同的多端平台 [1]  ，提供PC版，Web版，Mac版和手机版，支持手机和电脑间文件互传。 [2] 钉钉因中国企业而生，帮助中国企业通过系统化的解决方案（微应用），全方位提升中国企业沟通和协同效率。2019年5月10日，钉钉发布公告称，软件中类似“朋友圈”功能的社区、动态、朋友圈功能将暂停更新一个月 [3]  。2020年2月10日晚间，钉钉发布声明称，近期屡遭“PS图片造谣诋毁”，对这些连番多次的恶意污蔑中伤，钉钉已报警，坚决追究造谣传谣者的法律责任。 [4] 2020年3月，钉钉TV版登陆当贝市场首发上线。 [5] 2020年4月8日上午，阿里钉钉正式发布海外版DingTalk Lite，支持繁体中文、英文、日文等多种文字和语言，主要包括视频会议、群直播、聊天、日程等功能，疫情期间面向全球用户免费 [6]  。")

 if name == "微软":
     print(
        "微软 [1]  （英文名称：Microsoft；中文名称：微软公司或美国微软公司）始建于1975年，是一家美国跨国科技公司，也是世界PC（Personal Computer，个人计算机）软件开发的先导，由比尔·盖茨与保罗·艾伦创办于1975年，公司总部设立在华盛顿州的雷德蒙德（Redmond，邻近西雅图）。以研发、制造、授权和提供广泛的电脑软件服务业务为主。最为著名和畅销的产品为Microsoft Windows操作系统和Microsoft Office系列软件，目前是全球最大的电脑软件提供商。2018年4月22日，2017年全球最赚钱企业排行榜第15。 [2]  2018年5月29日，《2018年BrandZ全球最具价值品牌100强》第4位。 [3]  2018年7月19日，《财富》世界500强排行榜位列71位。 [4]  2018年12月18日，《2018世界品牌500强》第4位。 [5]  2019年6月，微软悄然删除其MS Celeb人脸识别数据库，微软称该数据库是全球最大的公开人脸识别数据库。 [6]  2019年7月，《财富》世界500强排行榜发布，微软位列60位。 [7]  2019福布斯全球数字经济100强榜排名第2位。 [8]  2019年10月，Interbrand发布的全球品牌百强排名第四位。 [9]  2020年1月22日，名列2020年《财富》全球最受赞赏公司榜单第3位。 [10] 2020年5月13日，微软名列2020福布斯全球企业2000强榜第13位。 [11-12] ")

 if name == "腾讯视频":
    print(
        "腾讯视频上线于2011年4月， [1]  是在线视频平台，拥有流行内容和专业的媒体运营能力 [2]  ，是聚合热播影视、综艺娱乐、体育赛事、新闻资讯等为一体的综合视频内容平台，并通过PC端、移动端及客厅产品等多种形态为用户提供高清流畅的视频娱乐体验。 [3-4] ")

 if name == "QQ音乐":
    print(
        "QQ音乐隶属于中国在线音乐服务领航者腾讯音乐娱乐集团，是国内领先的音乐流媒体平台。 [1-2]  自2005年创立至今，QQ音乐注册用户总量已达8亿。 [1-2] 以优质内容为核心，以大数据与互联网技术为推动力 [2]  ，QQ音乐致力于打造“智慧声态”的“立体”泛音乐生态圈 [3]  ，为用户提供多元化的音乐生活体验。2018年12月，通过技术检测以及用户举报发现，QQ音乐等18款APP疑似存在过度收集“短信”“通讯录”“位置”“录音”等用户敏感信息。 [4] 2019年11月8日，QQ音乐正式推出开放平台 [5]  。")

 if name == "酷我音乐":
    print(
        "酷我音乐 [1]  是在线数字音乐平台，自2005年成立以来，已经积累了领跑行业的版权曲库和无损音乐库。酷我音乐深挖综艺、影视、剧集等热门内容，通过主播电台、音乐直播、视频等特色内容，以及国际前沿的音频技术和高性价比音乐硬件产品，持续致力为用户提供个性化、多元化的音乐体验 [2]  。酷我音乐拥有曲库量近2000万首，与100余家唱片公司签署独家代理版权，还拥有中国好声音第一季、中国好声音第二季、蒙面歌王、燃烧吧少年、音乐大师课等综艺节目的独家版权。此外，太阳的后裔、青云志、好先生、亲爱的翻译官等热门影视剧的音乐原声也被酷我收入库中 [3]  。2018年9月，酷我音乐打造首档青年阅读分享类公益节目《榜样阅读》，持续挖掘平台潜力。将阅读与公益结合。 [4] 2015年9月推出第一款硬件产品酷我K1无线音乐耳机，酷我蓝牙音箱S7等多款硬件产品。 [5]  后续还将打造多款耳机音箱等高性能产品，围绕“畅听好音乐”打造音乐硬件链，完善其音乐生态布局 [6]  。")

 if name == "爱奇艺":
    print(
        "爱奇艺 [1]  是由龚宇于2010年4月22日创立的视频网站 [2]  ，2011年11月26日启动“爱奇艺”品牌并推出全新标志。爱奇艺成立伊始，坚持“悦享品质”的公司理念，以“用户体验”为生命，通过持续不断的技术投入、产品创新，为用户提供清晰、流畅、界面友好的观影体验。2013年5月7日百度收购PPS视频业务，并与爱奇艺进行合并，现为百度公司旗下平台。2018年3月29日，爱奇艺在美国纳斯达克挂牌上市，股票代码：IQ。在美国纽约时代广场，爱奇艺打出大幅广告庆祝上市 [3]  。 [4-5] 2018年8月6日，爱奇艺、新英体育建合资公司，统一运营爱奇艺体育； [6]  8月8日，爱奇艺获金运奖年度最佳创新运营奖。 [7]  9月3日，爱奇艺对外发布声明称，自即日起关闭显示全站前台播放量数据。 [8]  11月29日爱奇艺发布公告，计划发行总本金为5亿美元的可转换优先债券。 [9] 2019年6月11日，爱奇艺入选“2019福布斯中国最具创新力企业榜”。 [10-11]  2019年12月，爱奇艺入选2019中国品牌强国盛典榜样100品牌。 [12] ")

 if name == "unity":
    print(
        "Unity3D是由Unity Technologies开发的一个让玩家轻松创建诸如三维视频游戏、建筑可视化、实时三维动画等类型互动内容的多平台的综合型游戏开发工具，是一个全面整合的专业游戏引擎。Unity类似于Director,Blender game engine, Virtools 或 Torque Game Builder等利用交互的图型化开发环境为首要方式的软件。其编辑器可运行在Windows、Linux(目前仅支持Ubuntu和Centos发行版)、Mac OS X下，可发布游戏至Windows、Mac、Wii、iPhone、WebGL（需要HTML5）、Windows phone 8和Android平台。也可以利用Unity web player插件发布网页游戏，支持Mac和Windows的网页浏览。它的网页播放器也被Mac 所支持。")

 if name == "apple":
    print(
        "苹果公司（Apple Inc. ）是美国一家高科技公司。由史蒂夫·乔布斯、斯蒂夫·沃兹尼亚克和罗·韦恩(Ron Wayne)等人于1976年4月1日创立，并命名为美国苹果电脑公司（Apple Computer Inc. ），2007年1月9日更名为苹果公司，总部位于加利福尼亚州的库比蒂诺。苹果公司1980年12月12日公开招股上市，2012年创下6235亿美元的市值记录，截至2014年6月，苹果公司已经连续三年成为全球市值最大公司。苹果公司在2016年世界500强排行榜中排名第9名。 [1]  2013年9月30日，在宏盟集团的“全球最佳品牌”报告中，苹果公司超过可口可乐成为世界最有价值品牌。2014年，苹果品牌超越谷歌（Google），成为世界最具价值品牌。2016年9月8日凌晨1点，2016苹果秋季新品发布会在美国旧金山的比尔·格雷厄姆市政礼堂举行 [2]  。10月，苹果成为2016年全球100大最有价值品牌第一名。2017年1月6日早晨8点整，“红色星期五”促销活动在苹果官网正式上线，瞬间大量用户涌入官网进行抢购，仅两分钟所有参与活动的耳机便被抢光；2月，Brand Finance发布2017年度全球500强品牌榜单，苹果排名第二； [3]  6月7日，2017年《财富》美国500强排行榜发布，苹果排名第3位； [4]  7月20日，2017年世界500强排名第9位。 [5]  2018年12月18日，世界品牌实验室编制的《2018世界品牌500强》揭晓，苹果排名第3位。 [6] 2018年8月2日晚间，苹果盘中市值首次超过1万亿美元，股价刷新历史最高位至203.57美元。 [7]  入选2019《财富》世界500强、 [8]  2019福布斯全球数字经济100强榜第1位。 [9] ")

 if name == "苹果":
    print(
        "苹果公司（Apple Inc. ）是美国一家高科技公司。由史蒂夫·乔布斯、斯蒂夫·沃兹尼亚克和罗·韦恩(Ron Wayne)等人于1976年4月1日创立，并命名为美国苹果电脑公司（Apple Computer Inc. ），2007年1月9日更名为苹果公司，总部位于加利福尼亚州的库比蒂诺。苹果公司1980年12月12日公开招股上市，2012年创下6235亿美元的市值记录，截至2014年6月，苹果公司已经连续三年成为全球市值最大公司。苹果公司在2016年世界500强排行榜中排名第9名。 [1]  2013年9月30日，在宏盟集团的“全球最佳品牌”报告中，苹果公司超过可口可乐成为世界最有价值品牌。2014年，苹果品牌超越谷歌（Google），成为世界最具价值品牌。2016年9月8日凌晨1点，2016苹果秋季新品发布会在美国旧金山的比尔·格雷厄姆市政礼堂举行 [2]  。10月，苹果成为2016年全球100大最有价值品牌第一名。2017年1月6日早晨8点整，“红色星期五”促销活动在苹果官网正式上线，瞬间大量用户涌入官网进行抢购，仅两分钟所有参与活动的耳机便被抢光；2月，Brand Finance发布2017年度全球500强品牌榜单，苹果排名第二； [3]  6月7日，2017年《财富》美国500强排行榜发布，苹果排名第3位； [4]  7月20日，2017年世界500强排名第9位。 [5]  2018年12月18日，世界品牌实验室编制的《2018世界品牌500强》揭晓，苹果排名第3位。 [6] 2018年8月2日晚间，苹果盘中市值首次超过1万亿美元，股价刷新历史最高位至203.57美元。 [7]  入选2019《财富》世界500强、 [8]  2019福布斯全球数字经济100强榜第1位。 [9] ")

 if name == "小米":
    print(
        "小米手机是小米公司研发的高性能智能手机。Strategy Analytics发布2017年第二季度全球智能手机厂商出货量及市场份额报告显示，小米出货量2320万台，市场份额达到6.4%，重回世界前五。 [1] 2018年3月27日，小米首次在上海举行新品发布会，发布小米MIX2S。 [1]  2019年2月20日下午2点，小米在北京工业大学体育馆举行小米9发布会。 [2] ")

 if name == "Python":
    print(
        "Python是一种跨平台的计算机程序设计语言。 是一个高层次的结合了解释性、编译性、互动性和面向对象的脚本语言。最初被设计用于编写自动化脚本(shell)，随着版本的不断更新和语言新功能的添加，越多被用于独立的、大型项目的开发。")

 if name == "scratch":
    print(
        "Scratch是麻省理工学院的“终身幼儿园团队”开发的图形化编程工具，主要面对青少年开放。目前已有1.4版、2.0版本（增加克隆积木，视频侦测，Lego拓展积木）、3.0版本（增加文字朗读、翻译和Makey makey等选择性下载扩展积木，并增加micro:bit和Lego mindstorms EV3拓展积木）。所有人都可以在任意版本中创作自己的程序。")

 if name == "Scratch":
    print(
        "Scratch是麻省理工学院的“终身幼儿园团队”开发的图形化编程工具，主要面对青少年开放。目前已有1.4版、2.0版本（增加克隆积木，视频侦测，Lego拓展积木）、3.0版本（增加文字朗读、翻译和Makey makey等选择性下载扩展积木，并增加micro:bit和Lego mindstorms EV3拓展积木）。所有人都可以在任意版本中创作自己的程序。")

 if name == "C++":
    print(
        "是C语言的继承，它既可以进行C语言的过程化程序设计，又可以进行以抽象数据类型为特点的基于对象的程序设计，还可以进行以继承和多态为特点的面向对象的程序设计。C++擅长面向对象程序设计的同时，还可以进行基于过程的程序设计，因而C++就适应的问题规模而论，大小由之。 [1] C++不仅拥有计算机高效运行的实用性特征，同时还致力于提高大规模程序的编程质量与程序设计语言的问题描述能力。 [2] ")




def xxhelp():
    print("轩轩搜索库")
    print("版本号：1.0.0")
    print("轩轩工作室——————轩轩制作")
    print(" ")
    print("调用方法:xxsearchlib.baidu(name)")
    print("参数1 必填,搜索内容 ")
    print("返回参数：直接打开网址")
    print(" ")
    print(" ")
    print("库函数名称：")
    print(" ")
    print("1.百度搜索")
    print("  xxsearchlib.baidu(name)")
    print(" ")
    print("2.360搜索库")
    print("  xxsearchlib.so(name)")
    print(" ")
    print("3.搜狗搜索")
    print("  xxsearchlib.baidu(name)")
    print(" ")
    print("4.必应搜索")
    print("  xxsearchlib.bycn(name)")
    print(" ")
    print("5.MBA智搜")
    print("  xxsearchlib.MBA(name)")
    print(" ")
    print("6.爱奇艺搜索")
    print("  xxsearchlib.aiqiyi(name)")
    print(" ")
    print("7.搜了网搜索")
    print("  xxsearchlib.sole(name)")
    print(" ")
    print("8.微博搜索")
    print("  xxsearchlib.weibo(name)")
    print(" ")
    print("9.中国搜索")
    print("  xxsearchlib.cnso(name)")
    print(" ")
    print("10.淘宝搜索")
    print("  xxsearchlib.taobao(name)")
    print(" ")
    print("11.统一搜索")
    print("  xxsearchlib.ty(name)")
    print(" ")
    print("12.宜搜搜索")
    print("  xxsearchlib.easou(name)")
    print(" ")
    print(" ")
    print("13.轩轩搜索")
    print("  xxsearchlib.xxso(name)")
    print("  词条添加联系QQ：3603695237")
    print(" ")
    print("13.网址打开")
    print("  xxsearchlib.internet(name)")
    print(" ")
    print("示例代码会在1.2.0版本更新")
    print("持续更新中...")
    print("翻版、盗版、抄袭必究")
    print("作者QQ：3603695237")




