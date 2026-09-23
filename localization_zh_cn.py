"""
Simplified Chinese localization for Piko patches.

This script reads the upstream English strings.xml files and creates complete
zh-rCN translations. It preserves all existing upstream Chinese translations
(with corrections for known issues) and adds missing translations.

Called by build_piko.py after pre_build_cleanup() and before buildAndroid().
"""

import re
from pathlib import Path

# ── Twitter (piko_) translations ─────────────────────────────────────────────
# This dict maps English key -> Chinese translation for all 366 twitter keys.
# Existing upstream translations are preserved unless they have known issues.

TWITTER_ZH: dict[str, str] = {
    # ── Settings Search ──
    "piko_settings_search_hint": "搜索 Piko 设置",
    "piko_settings_search_clear": "清除输入",
    "piko_settings_search_no_results": "没有找到\"%s\"的相关设置",
    # ── Premium Settings ──
    "piko_title_premium": "Premium",
    "piko_pref_undo_posts": "启用撤销推文",
    "piko_pref_undo_posts_desc": "启用推文在发布前可以撤销的功能",
    "piko_pref_undo_posts_btn": "撤销推文设置",
    "piko_pref_icon_n_navbar_btn": "自定义导航和应用图标",
    "piko_pref_enable_force_pip": "强制小窗模式",
    "piko_pref_enable_force_pip_desc": "观看视频时进入后台可以画中画继续播放",
    # ── Download Settings ──
    "piko_title_download": "下载",
    "piko_pref_video_download": "视频下载",
    "piko_pref_download": "更改下载目录",
    "piko_pref_download_path": "主文件夹",
    "piko_pref_download_path_desc": "下载视频的主文件夹",
    "piko_pref_download_folder": "子文件夹",
    "piko_pref_download_folder_desc": "下载视频到 主文件夹/子文件夹",
    "piko_pref_download_media_link_handle": "下载视频设置",
    "piko_pref_download_media_link_handle_download": "直接下载视频",
    "piko_pref_download_media_link_handle_copy_link": "直接复制链接",
    "piko_pref_download_media_link_handle_always_ask": "每次都询问",
    "piko_pref_download_media_link_handle_copy_media_link": "复制链接",
    "piko_pref_download_media_link_handle_share_media_link": "分享链接",
    # ── Native ──
    "piko_title_native": "原生",
    "piko_title_native_downloader": "原生下载器",
    "piko_title_native_downloader_toggle": "启用原生下载器",
    "piko_pref_native_downloader_inline_button": "内嵌下载按钮",
    "piko_pref_native_downloader_inline_button_desc": "将下载按钮直接添加到帖子操作栏",
    "piko_pref_native_downloader_alert_title": "下载媒体",
    "piko_pref_native_downloader_download_all": "下载全部",
    "piko_pref_native_downloader_no_media": "未找到媒体",
    "piko_pref_native_downloader_filename_title": "保存文件名模式",
    "piko_pref_native_page_desc": "以下 Piko 原生功能可在帖子菜单中使用。",
    "piko_pref_native_downloader_autodownload_highest_video_res": "自动下载最高画质视频",
    "piko_pref_native_downloader_autodownload_highest_video_res_desc": "对于单个视频跳过选择窗口，直接下载当前可用的最高画质。",
    "piko_pref_native_downloader_show_download_icon": "显示下载图标",
    "piko_pref_native_downloader_show_copy_icon": "显示复制图标",
    "piko_pref_native_downloader_show_variants_icon": "显示画质选项图标",
    "piko_video_variants": "视频画质选项",
    "piko_browse_object_title": "浏览推文对象",
    # CORRECTED: was "启用浏览推送对象" → "启用浏览推文对象"
    "piko_browse_object_toggle": "启用浏览推文对象",
    "piko_share_image_title": "分享截图",
    # CORRECTED: was "启用分享截屏" → "启用分享帖子截图"
    "piko_share_image_toggle": "启用分享帖子截图",
    "piko_share_image_autocleanup": "自动清理截屏",
    "piko_share_image_autocleanup_desc": "启用后将删除 24 小时前的截屏",
    "piko_share_image_invalid_context": "无效的上下文",
    "piko_share_image_capturing": "正在生成帖子截图……",
    "piko_share_image_view_not_found": "未找到帖子视图",
    "piko_share_image_capture_failed": "截图失败",
    "piko_share_image_error": "错误：%s",
    "piko_share_image_app_error": "未找到 %s",
    "piko_share_image_instagram_stories": "分享到 Instagram 快拍",
    "piko_share_image_whatsapp_status": "分享到 WhatsApp 状态",
    "piko_title_native_share_menu": "原生分享菜单",
    "piko_native_share_menu_toggle": "启用原生分享菜单",
    "piko_title_native_translator": "原生帖子翻译",
    "piko_native_translator_toggle": "启用原生帖子翻译",
    "piko_native_translator_provider": "翻译服务",
    "piko_native_translator_to_lang": "目标语言",
    "piko_native_translator_zero_text": "未找到需要翻译的文本",
    "piko_native_translator_google": "Google 翻译",
    "piko_native_translator_google_v2": "Google 翻译 V2",
    "piko_native_translator_fxtwitter": "FxTwitter API",
    "piko_title_native_reader_mode": "原生阅读器模式",
    "piko_native_reader_mode_toggle": "启用原生阅读器模式",
    "piko_native_reader_mode_grok_thread": "分析此主题",
    "piko_native_reader_mode_grok_author": "更多关于作者",
    "piko_native_reader_mode_source": "来源",
    "piko_native_reader_mode_published": "发布",
    "piko_native_reader_mode_total_post": "推文总数",
    "piko_native_reader_mode_pref_text_only_mode": "纯文本模式",
    "piko_native_reader_mode_pref_hide_quoted_posts": "隐藏引用推文",
    "piko_native_reader_mode_pref_no_grok": "无 Grok 分析",
    "piko_native_reader_mode_copy_post": "复制推文链接",
    "piko_native_reader_mode_cache_delete": "删除阅读器缓存",
    "piko_native_reader_mode_cache_delete_success": "缓存删除成功",
    "piko_native_reader_mode_cache_delete_failed": "缓存删除失败",
    # ── Ads Settings ──
    "piko_title_ads": "广告",
    "piko_pref_hide_promoted_posts": "隐藏推广帖子",
    "piko_pref_wtf_section": "隐藏推荐关注",
    "piko_pref_cts_section": "隐藏创作者推荐",
    "piko_pref_ctj_section": "隐藏探索社群",
    "piko_pref_ryb_section": "隐藏重新访问你的书签",
    "piko_pref_pinned_posts_section": "隐藏已由你关注的人置顶",
    "piko_pref_hide_premium_prompt": "隐藏信息推广",
    "piko_pref_hide_todays_news": "隐藏今日新闻",
    "piko_pref_del_from_db": "从数据库中删除项目",
    "piko_pref_db_promoted_posts": "推广帖子",
    "piko_pref_db_wtf_section": "推荐关注",
    "piko_pref_db_cts_section": "创作者推荐",
    "piko_pref_db_ctj_section": "探索社群",
    "piko_pref_db_ryb_section": "重新访问你的书签",
    "piko_pref_db_pinned_posts_section": "已由你关注的人置顶",
    "piko_pref_db_premium_prompt": "信息推广",
    "piko_pref_db_todays_news": "今日新闻",
    "piko_pref_db_not_found": "未找到数据库",
    "piko_pref_db_not_open": "未打开数据库",
    "piko_pref_db_del_items": "删除的项目",
    "piko_pref_hide_premium_upsell": "隐藏升级订阅",
    "piko_pref_hide_premium_upsell_desc": "移除首页顶部升级 Premium 按钮",
    "piko_pref_top_people_search": "隐藏搜索热门用户",
    "piko_pref_top_people_search_desc": "隐藏搜索结果热门中的用户",
    # ── Misc Settings ──
    "piko_title_misc": "杂项",
    "piko_pref_hide_fab": "隐藏发推按钮",
    "piko_pref_hide_fab_menu": "隐藏发推按钮菜单",
    "piko_pref_rec_users": "隐藏推荐用户",
    "piko_pref_hide_view_count": "隐藏查看次数",
    "piko_pref_custom_share_domain": "自定义分享域名",
    "piko_pref_custom_share_domain_desc": "自定义分享帖子时使用的域名",
    "piko_pref_show_sensitive_media": "显示敏感媒体",
    "piko_pref_selectable_text": "可选文本",
    "piko_pref_clear_tracking_params": "清除跟踪参数",
    "piko_pref_unshorten_link": "不使用短网址",
    "piko_pref_unshorten_link_desc": "移除 t.co 短网址",
    "piko_pref_round_off_numbers": "数字简化显示",
    "piko_pref_round_off_numbers_desc": "将数字简化为以万为单位显示",
    "piko_pref_debug_menu": "启用帖子调试菜单",
    "piko_pref_quick_settings": "启用快捷设置",
    "piko_pref_quick_settings_summary": "在侧边栏添加快捷设置按钮",
    "piko_pref_pause_search_suggestion": "暂停搜索建议",
    "piko_pref_pause_search_suggestion_desc": "将不会在本地保存搜索建议",
    "piko_pref_search_suggestion": "隐藏搜索建议",
    "piko_pref_search_suggestion_desc": "隐藏探索页面中的搜索建议",
    "piko_legacy_share_link": "旧版分享链接",
    "piko_pref_hide_unrelated_replies": "隐藏无关回复",
    "piko_pref_db_unrelated_replies": "无关回复",
    "piko_pref_chirp_font": "禁用 Chirp 字体",
    "piko_block_redirecting_to_x_lite": "阻止跳转到 X Lite",
    # ── Feature flags Settings ──
    "piko_title_feature_flags": "功能标志",
    "piko_pref_feature_flags": "新增功能标志",
    "piko_pref_edit_flag_title": "编辑标志",
    "piko_pref_add_flag_title": "添加标志",
    "piko_pref_search_flags": "搜索标志",
    "piko_pref_import_flags": "导入标志",
    "piko_pref_export_flags": "导出标志",
    "piko_pref_reset_flags": "重置标志",
    # ── Timeline Settings ──
    "piko_title_timeline": "时间线",
    "piko_pref_disable_auto_timeline_scroll": "启动时保持时间线位置",
    "piko_pref_show_post_source": "显示推文来源标签",
    "piko_pref_show_post_source_desc": "打开推文信息时可能会有延迟，并且标签仅会在公开推文中显示",
    "piko_pref_hide_live_threads": "隐藏直播空间",
    "piko_pref_hide_live_threads_desc": "移除顶部直播通知条",
    "piko_pref_hide_banner": "隐藏新帖子",
    "piko_pref_hide_banner_desc": "隐藏弹出的新帖按钮",
    "piko_pref_hide_bmk_timeline": "隐藏时间线中的书签图标",
    "piko_pref_force_translate": "强制显示翻译按钮",
    "piko_pref_force_translate_desc": "始终为您显示翻译帖子按钮",
    "piko_pref_hide_quick_promote": "隐藏推广按钮",
    "piko_pref_hide_quick_promote_desc": "移除自己帖子下的推广按钮",
    "piko_pref_show_poll_result": "显示投票结果",
    "piko_pref_show_poll_result_desc": "无需投票即可查看投票结果",
    "piko_pref_hide_community_notes": "隐藏社群附注",
    "piko_pref_hide_immersive_player": "隐藏沉浸式播放器",
    "piko_pref_hide_immersive_player_desc": "移除视频向上滑动查看更多",
    "piko_pref_enable_vid_auto_advance": "启用视频自动滚动",
    "piko_pref_enable_vid_auto_advance_desc": "启用视频自动滚动查看更多",
    "piko_pref_hide_hidden_replies": "隐藏隐藏的回复",
    "piko_pref_force_hd": "强制高清视频",
    "piko_pref_force_hd_desc": "始终选择播放可用最高画质",
    "piko_pref_hide_nudge_button": "隐藏社交按钮",
    "piko_pref_hide_nudge_button_desc": "隐藏帖子上的关注/订阅/回关按钮",
    "piko_pref_hide_social_proof": "隐藏社交关系",
    "piko_pref_hide_social_proof_desc": "隐藏他人主页上的谁关注了此账号",
    "piko_pref_hide_community_badge": "隐藏社群徽章",
    "piko_pref_hide_badge_nav_bar": "隐藏导航栏徽章",
    "piko_pref_hide_badge_nav_bar_desc": "隐藏导航栏图标上的通知提示和计数",
    "piko_pref_hide_post_inline_metrics": "隐藏帖子互动数",
    "piko_pref_hide_post_inline_metrics_desc": "隐藏帖子点赞、转帖等次数",
    "piko_pref_hide_post_detailed_metrics": "隐藏帖子详情页互动量",
    "piko_pref_hide_post_detailed_metrics_desc": "在帖子详情页中隐藏点赞、转帖等次数",
    # ── Customization Settings ──
    "piko_title_customisation": "自定义",
    "piko_pref_customisation_profiletabs": "隐藏个人资料标签",
    "piko_pref_customisation_timelinetabs": "隐藏时间线标签",
    "piko_pref_customisation_timelinetabs_foryou": "移除为你推荐",
    "piko_pref_customisation_timelinetabs_following": "移除正在关注",
    "piko_pref_customisation_timelinetabs_both": "默认同时显示",
    "piko_pref_customisation_sidebartabs": "隐藏侧边栏项目",
    "piko_pref_customisation_navbartabs": "隐藏导航栏项目",
    "piko_pref_customisation_inlinetabs": "隐藏互动栏项目",
    "piko_pref_customisation_exploretabs": "隐藏探索栏标签",
    "piko_pref_customisation_searchtabs": "隐藏搜索结果标签",
    "piko_pref_customisation_notificationtabs": "隐藏通知标签",
    "piko_pref_customisation_reply_sorting": "选择默认回复排序",
    "piko_pref_customisation_reply_sorting_remember": "保持选择",
    "piko_pref_customisation_post_font_size": "帖子字体大小",
    "piko_pref_customisation_search_type_ahead": "隐藏搜索建议",
    "piko_pref_customisation_change_app_icon": "更改应用图标",
    "piko_pref_customisation_more_info_on_profile": "个人资料更多信息",
    "piko_pref_customisation_more_info_on_profile_desc": "在个人资料页面显示更多信息",
    "piko_pref_dynamic_color": "动态取色",
    "piko_pref_dynamic_color_desc": "将系统 Material You 配色应用到全局主题。若要为应用图标启用动态颜色，请进入 Piko 设置 > 自定义 > 更改应用图标",
    # ── Font Settings ──
    "piko_title_font": "字体样式",
    "piko_pref_add_font": "添加字体",
    "piko_pref_add_font_desc": "请确保字体为 .ttf 或 .otf 格式",
    "piko_pref_delete_font": "删除字体",
    "piko_pref_add_emoji_font": "添加表情符号",
    "piko_pref_delete_emoji_font": "删除表情符号",
    "piko_pref_add_font_success": "字体添加成功",
    "piko_pref_add_font_fail": "字体添加失败",
    "piko_pref_delete_font_success": "字体删除成功",
    "piko_pref_delete_font_fail": "字体删除失败",
    "piko_pref_delete_font_warn": "未找到可删除的自定义字体",
    # ── External Downloader ──
    "piko_pref_external_downloader_toggle": "启用外部下载器",
    "piko_pref_external_downloader_text": "使用外部下载器下载",
    "piko_pref_external_downloader_package_name": "外部下载器包名",
    "piko_pref_external_downloader_package_not_set": "未设置外部下载器包名",
    "piko_pref_external_downloader_package_not_found": "找不到外部下载器",
    # ── Logging Settings ──
    "piko_title_logging": "日志记录",
    "piko_pref_server_response_logging": "记录服务器响应",
    "piko_pref_server_response_logging_desc": "记录从服务器收到的 JSON 响应，保存在 \'Download/Piko\' 文件夹中",
    "piko_pref_server_response_logging_file_overwrite": "覆盖响应日志文件",
    "piko_pref_server_response_logging_file_overwrite_desc": "启动时清除现有的响应日志数据",
    # ── Backup and Restore ──
    "piko_title_backup": "备份和恢复",
    "piko_pref_import_settings": "导入Piko设置",
    "piko_pref_export_settings": "导出Piko设置",
    "piko_pref_reset_settings": "重置Piko设置",
    "piko_pref_export_success": "导出成功",
    "piko_pref_import_success": "导入成功",
    "piko_pref_export_failed": "错误：导出%s失败",
    "piko_pref_import_failed": "错误：导入%s失败",
    "piko_pref_export_no_uri": "错误：未提供目标",
    "piko_pref_import_no_uri": "错误：未提供文件",
    "piko_pref_export_login_token": "导出登录令牌",
    "piko_pref_import_login_token": "导入登录令牌",
    # ── About ──
    "piko_title_about": "关于",
    # CORRECTED: was "App 版本" → "应用版本"
    "piko_pref_app_version": "应用版本",
    "piko_pref_patch_info": "Piko 补丁信息",
    "piko_pref_version_info": "版本信息",
    "piko_changelogs_title": "变更日志",
    # CORRECTED: was "补丁" → "Piko 补丁"
    "piko_pref_patches": "Piko 补丁",
    "piko_pref_included": "包括",
    "piko_pref_excluded": "排除",
    "piko_pref_app_restart_rec": "建议更改后重新启动应用",
    "piko_dialog_delete_title": "删除",
    "piko_dialog_delete_message": "删除%s?",
    "piko_pref_search_type_ahead_users": "用户",
    "piko_pref_search_type_ahead_events": "事件",
    "piko_pref_search_type_ahead_ordered_section": "订购",
    "piko_settings_supported_links": "打开支持的链接",
    "piko_notifications_tab_priority": "优先级",
    "piko_fast_follower": "快速关注者",
    "piko_debug": "Piko 调试",
    # ── Arrays ──
    "piko_array_grok": "Grok",
    "piko_array_money": "Money",
    "piko_array_xchat": "X Chat",
    "piko_array_x_lite": "全新 X Android",
    "piko_array_conference": "会议",
    "piko_array_creator_studio": "创作者工作室",
    "piko_array_jobs": "职位",
    "piko_array_media": "媒体",
    "piko_array_light_mode": "日间模式",
    # ── App icon strings ──
    "piko_app_icon_thanks": "感谢 @NeoFreeBird 提供 iOS 应用图标",
    "piko_app_icon_piko_exclusive": "（Piko 独家）",
    # Category
    "piko_app_icon_category_legacy": "经典",
    "piko_app_icon_category_seasonal_event": "季节活动",
    "piko_app_icon_category_sports": "体育",
    "piko_app_icon_category_cultural_and_celebrations": "文化和庆典",
    "piko_app_icon_category_pride": "骄傲月",
    "piko_app_icon_category_misc": "其他",
    "piko_app_icon_category_space": "太空",
    "piko_app_icon_category_movies_n_series": "影视",
    # Icon names
    "piko_app_icon_name_default": "默认",
    "piko_app_icon_name_legacy_icon_1": "经典图标 一",
    "piko_app_icon_name_legacy_icon_2": "经典图标 二",
    "piko_app_icon_name_legacy_icon_3": "经典图标 三",
    "piko_app_icon_name_legacy_icon_4": "经典图标 四",
    "piko_app_icon_name_legacy_blue": "经典蓝",
    "piko_app_icon_name_twitter_blue": "推特蓝",
    "piko_app_icon_name_earth": "地球",
    "piko_app_icon_name_moon": "月球",
    "piko_app_icon_name_mars": "火星",
    "piko_app_icon_name_sun": "太阳",
    "piko_app_icon_name_stars": "星星",
    "piko_app_icon_name_milky_way": "银河",
    "piko_app_icon_name_autumn_2021": "秋天 2021",
    "piko_app_icon_name_autumn_2022": "秋天 2022",
    "piko_app_icon_name_south_spring_2021": "南春 2021",
    "piko_app_icon_name_south_spring_2022": "南春 2022",
    "piko_app_icon_name_winter_1": "冬天 1",
    "piko_app_icon_name_winter_2": "冬天 2",
    "piko_app_icon_name_summer_1": "夏天 1",
    "piko_app_icon_name_summer_2": "夏天 2",
    "piko_app_icon_name_autumn_southern": "南秋",
    "piko_app_icon_name_summer": "夏天",
    "piko_app_icon_name_winter": "冬天",
    "piko_app_icon_name_beijing_olympics_1": "北京奥运会 1",
    "piko_app_icon_name_beijing_olympics_2": "北京奥运会 2",
    "piko_app_icon_name_daytona": "戴通纳赛车",
    "piko_app_icon_name_formulaone": "F1",
    "piko_app_icon_name_kentucky_derby": "肯塔基德比",
    "piko_app_icon_name_mlb": "MLB",
    "piko_app_icon_name_nba": "NBA",
    "piko_app_icon_name_nba_2": "NBA 2",
    "piko_app_icon_name_ncaa": "NCAA",
    "piko_app_icon_name_masters": "美国大师赛",
    "piko_app_icon_name_nba_finals": "NBA 决赛",
    "piko_app_icon_name_stanley_cup": "斯坦利杯",
    "piko_app_icon_name_commonwealth": "英联邦",
    "piko_app_icon_name_mothers_day": "母亲节",
    "piko_app_icon_name_womansday": "妇女节",
    "piko_app_icon_name_halloween_2021": "万圣节 2021",
    "piko_app_icon_name_halloween_2022": "万圣节 2022",
    "piko_app_icon_name_halloween_2024_1": "万圣节 2024 1",
    "piko_app_icon_name_halloween_2024_2": "万圣节 2024 2",
    "piko_app_icon_name_halloween_2024_3": "万圣节 2024 3",
    "piko_app_icon_name_holi": "酒红节",
    "piko_app_icon_name_stpatricks_day": "圣帕特里克节",
    "piko_app_icon_name_easter": "复活节",
    "piko_app_icon_name_anzac": "澳新军团",
    "piko_app_icon_name_ramadan": "斋月",
    "piko_app_icon_name_black_history": "黑色历史",
    "piko_app_icon_name_eurovisionfinal": "欧洲歌唱大赛决赛",
    "piko_app_icon_name_lunar_new_year_1": "农历新年 1",
    "piko_app_icon_name_lunar_new_year_2": "农历新年 2",
    "piko_app_icon_name_japanese_new_year_2024_1": "日本新年 2024 1",
    "piko_app_icon_name_japanese_new_year_2024_2": "日本新年 2024 2",
    "piko_app_icon_name_may_the_fourth": "星际大战日",
    "piko_app_icon_name_barbie": "芭比",
    "piko_app_icon_name_thanksgiving_1": "感恩节 1",
    "piko_app_icon_name_thanksgiving_2": "感恩节 2",
    "piko_app_icon_name_thanksgiving_2024_1": "感恩节 2024 1",
    "piko_app_icon_name_thanksgiving_2024_2": "感恩节 2024 2",
    "piko_app_icon_name_thanksgiving_2024_3": "感恩节 2024 3",
    "piko_app_icon_name_thanksgiving_2024_4": "感恩节 2024 4",
    "piko_app_icon_name_thanksgiving_2024_5": "感恩节 2024 5",
    "piko_app_icon_name_thanksgiving_2024_6": "感恩节 2024 6",
    "piko_app_icon_name_canada_day": "加拿大日",
    "piko_app_icon_name_canada_indigenous": "加拿大土著",
    "piko_app_icon_name_earth_hour": "地球一小时",
    "piko_app_icon_name_euro": "欧洲",
    "piko_app_icon_name_independence_day": "独立日",
    "piko_app_icon_name_juneteenth": "解放黑奴纪念日",
    "piko_app_icon_name_naidoc": "Naidoc Week",
    "piko_app_icon_name_christmas_2024_1": "圣诞节 2024 1",
    "piko_app_icon_name_christmas_2024_2": "圣诞节 2024 2",
    "piko_app_icon_name_christmas_2024_3": "圣诞节 2024 3",
    "piko_app_icon_name_christmas_2024_4": "圣诞节 2024 4",
    "piko_app_icon_name_upsidedown": "逆世界",
    "piko_app_icon_name_games_chamber": "天地逃生",
    "piko_app_icon_name_pridesouthern": "南方骄傲组织",
    "piko_app_icon_name_newzealand_pride_1": "新西兰的骄傲 1",
    "piko_app_icon_name_newzealand_pride_2": "新西兰的骄傲 2",
    "piko_app_icon_name_pride_month": "骄傲月",
    "piko_app_icon_name_fancy": "Fancy",
    "piko_app_icon_name_broken": "碎裂",
    "piko_app_icon_name_cyber": "赛博",
    "piko_app_icon_name_soft_pastel_pink": "柔粉",
    "piko_app_icon_name_electric_indigo": "Electric Indigo",
    "piko_app_icon_name_neon_pink": "霓虹粉",
    "piko_app_icon_name_tropical_teal": "热带青色",
    "piko_app_icon_name_vivid_orange": "鲜活橙",
    "piko_app_icon_name_material_you": "Material You",
    # ── Import / export login tokens ──
    "piko_login_token_select_account": "选择账号：",
    "piko_login_token_export_copy_to_clipboard": "复制到剪贴板",
    "piko_login_token_export_save_to_file": "保存到文件",
    "piko_login_token_export_no_accounts_message": "提示：当前没有登录任何账号。要导出令牌，请先登录账号。",
    "piko_login_token_import_token_button_text": "通过令牌登录",
    "piko_login_token_import_from_text": "从文本导入",
    "piko_login_token_import_from_file": "从文件导入",
    "piko_login_token_import_about": "关于此功能 (打开网站)",
    "piko_login_token_import_success_reopen_required": "请重新打开应用",
    "piko_login_token_import_failed_missing_info": "错误：\"username\" 或 \"token\" 或 \"secret\" 丢失",
    "piko_login_token_import_failed_already_exist": "添加账户失败（可能已存在）",
    # Long description – keep GitHub URL intact
    "piko_login_token_export_screen_description": (
        "此功能用于导出当前已登录账号的会话令牌。\n\n"
        "警告：导出的令牌属于高度机密信息。\n"
        "切勿将其分享给任何人！\n"
        "如果他人获取了此令牌，他们可以在您退出登录前自由访问您的账号。\n\n"
        "详情请参阅此页面。\n"
        "https://github.com/crimera/piko/blob/dev/docs/about_login_token_patch.md\n"
        "建议在使用此功能前阅读上述文档，其中包含一些重要信息，例如如何导入令牌。"
    ),
    # ── Common ──
    "piko_ok": "确定",
    "piko_cancel": "取消",
}

# ── NewX (piko_newx_) translations ──────────────────────────────────────────
# All 410 newx keys need zh-CN translations since upstream has none.

NEWX_ZH: dict[str, str] = {
    # Settings title / common
    "piko_newx_settings_title": "Piko 设置",
    "piko_newx_settings_ok": "确定",
    "piko_newx_settings_cancel": "取消",
    "piko_newx_patch_version": "Piko %s",
    "piko_newx_settings_open_failed": "无法打开 Piko NewX 设置",
    "piko_newx_settings_search_hint": "搜索设置",
    "piko_newx_settings_search_clear": "清除搜索",
    "piko_newx_settings_search_no_results": "没有找到\"%s\"的相关设置",
    "piko_newx_action_failed": "NewX 设置操作失败",
    "piko_newx_restart_title": "重启 X？",
    "piko_newx_restart_summary": "立即重启应用以应用此更改。",
    "piko_newx_restart_now": "立即重启",
    "piko_newx_setting_validation_failed": "无法验证此设置",
    "piko_newx_patch_version": "Piko %s",
    # Categories
    "piko_newx_category_timeline_title": "时间线",
    "piko_newx_category_timeline_summary": "管理时间线行为和外观",
    "piko_newx_category_content_title": "内容",
    "piko_newx_category_content_summary": "控制推广、推荐、敏感媒体和过滤规则",
    "piko_newx_category_appearance_title": "外观",
    "piko_newx_category_appearance_summary": "自定义颜色和字体",
    "piko_newx_category_post_actions_media_title": "帖子和媒体",
    "piko_newx_category_post_actions_media_summary": "自定义帖子操作、回复、媒体标签、下载和分享",
    "piko_newx_category_navigation_title": "导航",
    "piko_newx_category_navigation_summary": "自定义导航栏和抽屉项目",
    "piko_newx_category_advanced_title": "高级",
    "piko_newx_category_advanced_summary": "高级用户工具、调试和设置维护",
    # Timeline
    "piko_newx_disable_timeline_refresh_title": "禁止自动刷新时间线",
    "piko_newx_disable_timeline_refresh_summary": "防止 NewX 启动或返回前台时时间线跳动",
    "piko_newx_hide_timeline_tabs_title": "隐藏时间线标签栏",
    "piko_newx_hide_timeline_tabs_summary": "移除 NewX 首页时间线上的\"为你推荐\"和\"正在关注\"标签栏",
    "piko_newx_timeline_tabs_title": "要隐藏的时间线标签",
    "piko_newx_timeline_tabs_summary": "选择要隐藏的首页时间线标签",
    "piko_newx_timeline_tabs_hide_for_you": "隐藏为你推荐",
    "piko_newx_timeline_tabs_hide_following": "隐藏正在关注",
    "piko_newx_timeline_tabs_show_both": "同时显示",
    "piko_newx_restore_timeline_position_title": "恢复时间线位置",
    "piko_newx_restore_timeline_position_summary": "应用重启后恢复\"为你推荐\"和\"正在关注\"的滚动位置",
    "piko_newx_for_you_tab_hook_title": "使用自定义推荐话题选择器",
    "piko_newx_for_you_tab_hook_summary": "从\"为你推荐\"标签打开自定义话题选择器，而非原生的暂停推荐面板",
    # Content
    "piko_newx_filter_promoted_posts_title": "过滤推广帖子",
    "piko_newx_filter_promoted_posts_summary": "移除推广帖子和推广时间线模块",
    "piko_newx_hide_who_to_follow_title": "隐藏推荐关注",
    "piko_newx_hide_who_to_follow_summary": "移除时间线和主页上的推荐用户板块",
    "piko_newx_hide_discover_more_title": "隐藏\"发现更多\"",
    "piko_newx_hide_discover_more_summary": "移除帖子详情时间线中的\"发现更多\"板块",
    "piko_newx_hide_premium_upsell_title": "隐藏 Premium 推广",
    "piko_newx_hide_premium_upsell_summary": "隐藏首页顶部栏中的 Premium 升级提示",
    "piko_newx_hide_grok_title": "隐藏 Grok 按钮",
    "piko_newx_hide_grok_summary": "移除帖子、帖子详情和主页头部的 Grok 按钮",
    "piko_newx_hide_spaces_bar_title": "隐藏 Spaces 栏",
    "piko_newx_hide_spaces_bar_summary": "隐藏 NewX 时间线上方的 Spaces 栏",
    "piko_newx_hide_new_post_button_title": "隐藏发帖按钮",
    "piko_newx_hide_new_post_button_summary": "移除 NewX 时间线上的发帖（撰写新帖）按钮",
    "piko_newx_hide_new_post_pill_title": "隐藏新帖提示",
    "piko_newx_hide_new_post_pill_summary": "隐藏有新帖可用时出现的胶囊提示",
    "piko_newx_hide_post_dividers_title": "隐藏帖子分隔线",
    "piko_newx_hide_post_dividers_summary": "移除 NewX 时间线中帖子和串回复之间的分隔线",
    "piko_newx_hide_post_reply_bar_title": "隐藏帖子回复栏",
    "piko_newx_hide_post_reply_bar_summary": "隐藏帖子详情页中固定的回复栏，同时保留发帖按钮",
    "piko_newx_show_sensitive_media_title": "显示敏感媒体",
    "piko_newx_show_sensitive_media_summary": "无需确认即可显示敏感媒体",
    "piko_newx_show_poll_results_title": "无需投票查看投票结果",
    "piko_newx_show_poll_results_summary": "投票结果可用时，在投票前显示投票百分比",
    "piko_newx_hide_ai_generated_posts_title": "隐藏 AI 生成帖子",
    "piko_newx_hide_ai_generated_posts_summary": "从 NewX 时间线中隐藏选定的 AI 生成帖子",
    "piko_newx_hide_ai_generated_posts_auto_detected": "自动检测",
    "piko_newx_hide_ai_generated_posts_user_marked": "用户标记",
    "piko_newx_hide_ai_generated_posts_source_not_identified": "AI 来源未识别",
    "piko_newx_topic_filtering_title": "推荐话题过滤",
    "piko_newx_topic_filtering_summary": "选择从 X 运行时发现的话题",
    "piko_newx_topic_filtering_empty": "尚未发现任何话题。请打开\"为你推荐\"时间线，然后返回此页面。",
    "piko_newx_topic_filter_enabled_title": "启用话题过滤",
    "piko_newx_topic_filter_enabled_summary": "使用选定的正向话题 ID，不设原生暂停推荐过期时间",
    # Verified account filtering
    "piko_newx_group_verified_account_filtering_title": "认证账号过滤",
    "piko_newx_group_verified_account_filtering_summary": "按时间线报告的账号认证类型过滤帖子",
    "piko_newx_hide_verified_account_types_title": "按认证类型隐藏帖子",
    "piko_newx_hide_verified_account_types_summary": "隐藏时间线数据中报告为选定认证类型的帖子和回复",
    "piko_newx_hide_verified_account_types_business": "企业",
    "piko_newx_hide_verified_account_types_government": "政府",
    "piko_newx_hide_verified_account_types_user": "用户 / 蓝标认证",
    "piko_newx_hide_verified_account_types_unknown": "未知",
    "piko_newx_verified_account_timeline_filter_title": "启用时间线过滤",
    "piko_newx_verified_account_timeline_filter_summary": "从常规时间线中隐藏选定的认证账号类型",
    "piko_newx_verified_account_thread_filter_title": "启用对话串过滤",
    "piko_newx_verified_account_thread_filter_summary": "从对话串中隐藏选定的认证账号类型",
    "piko_newx_verified_account_filtered_replies_menu_title": "显示\"已过滤回复\"菜单",
    "piko_newx_verified_account_filtered_replies_menu_summary": "当对话串过滤开启时，在帖子菜单中添加\"已过滤回复\"选项",
    "piko_newx_verified_account_whitelist_title": "认证账号白名单",
    "piko_newx_verified_account_whitelist_summary": "当选定账号的时间线认证类型被隐藏时，保持其可见。输入 @用户名或数字账号 ID。",
    "piko_newx_verified_account_whitelist_add_title": "添加认证账号",
    "piko_newx_verified_account_whitelist_account_hint": "@用户名或数字账号 ID",
    "piko_newx_verified_account_whitelist_add": "添加账号",
    "piko_newx_verified_account_whitelist_save": "保存",
    "piko_newx_verified_account_whitelist_cancel": "取消",
    "piko_newx_verified_account_whitelist_empty": "暂无白名单账号。\n\n添加 @用户名或数字账号 ID。长按账号可将其移除。",
    "piko_newx_verified_account_whitelist_error_blank": "请输入账号用户名或数字账号 ID。",
    "piko_newx_verified_account_whitelist_error_duplicate": "该账号已在白名单中。",
    # Filtered replies
    "piko_newx_filtered_replies_dialog_title": "已过滤回复",
    "piko_newx_filtered_replies_option_label": "已过滤回复",
    "piko_newx_filtered_replies_empty": "此帖子没有已过滤的回复。",
    "piko_newx_filtered_replies_copied": "已复制回复文本",
    "piko_newx_filtered_replies_whitelist_add": "+ 加入白名单",
    "piko_newx_filtered_replies_whitelist_added": "已将 @%s 加入白名单",
    "piko_newx_filtered_replies_whitelisted": "已在白名单 ✓",
    # Post filtering
    "piko_newx_post_filtering_title": "帖子过滤",
    "piko_newx_post_filtering_summary": "隐藏包含用户自定义词语和短语的帖子",
    "piko_newx_post_filtering_enabled_title": "启用帖子过滤",
    "piko_newx_post_filtering_add_title": "添加过滤规则",
    "piko_newx_post_filtering_edit_title": "编辑过滤规则",
    "piko_newx_post_filtering_add": "添加过滤规则",
    "piko_newx_post_filtering_save": "保存",
    "piko_newx_post_filtering_cancel": "取消",
    "piko_newx_post_filtering_remove": "移除",
    "piko_newx_post_filtering_empty": "暂无过滤规则。\n\n规则匹配字面词语或短语，不区分大小写。内容规则检查帖子、引用、注释、文章和链接卡片。用户名规则检查帖子和引用的作者。匹配内容将从新加载的时间线中隐藏，包括回复和主页时间线。",
    "piko_newx_post_filtering_phrase_hint": "词语或短语",
    "piko_newx_post_filtering_match_content": "匹配帖子内容",
    "piko_newx_post_filtering_match_usernames": "匹配用户名",
    "piko_newx_post_filtering_scope_both": "帖子内容和用户名",
    "piko_newx_post_filtering_scope_content": "帖子内容",
    "piko_newx_post_filtering_scope_usernames": "用户名",
    "piko_newx_post_filtering_error_blank": "请输入词语或短语。",
    "piko_newx_post_filtering_error_duplicate": "该词语或短语已有规则。",
    "piko_newx_post_filtering_error_scope": "请至少选择一种匹配范围。",
    "piko_newx_post_filtering_rule_enabled": "过滤规则已启用",
    # Appearance
    "piko_newx_dynamic_color_title": "使用动态取色",
    "piko_newx_dynamic_color_summary": "在 NewX 和 Piko 设置中使用系统 Material You 配色。",
    "piko_newx_dynamic_color_amoled_title": "AMOLED 纯黑",
    "piko_newx_dynamic_color_amoled_summary": "在深色模式下使用纯黑背景。",
    "piko_newx_dynamic_color_like_title": "为已点赞帖子着色",
    "piko_newx_dynamic_color_like_summary": "为已点赞帖子使用动态强调色。注意：这会禁用红心 Lottie 动画。",
    "piko_newx_font_title": "字体样式",
    "piko_newx_font_summary": "自定义应用和表情符号字体样式",
    "piko_newx_system_font_title": "使用系统字体",
    "piko_newx_system_font_summary": "使用默认系统字体",
    "piko_newx_add_font_title": "添加字体",
    "piko_newx_add_font_summary": "请确保字体为 .ttf 或 .otf 格式",
    "piko_newx_add_emoji_font_title": "添加表情符号字体",
    "piko_newx_add_emoji_font_summary": "请确保字体为 .ttf 或 .otf 格式",
    "piko_newx_delete_font_title": "删除字体",
    "piko_newx_delete_emoji_font_title": "删除表情符号字体",
    "piko_newx_custom_font_title": "自定义字体",
    "piko_newx_custom_font_summary": "为应用应用自定义 TTF 或 OTF 字体",
    "piko_newx_custom_emoji_font_title": "自定义表情符号字体",
    "piko_newx_custom_emoji_font_summary": "为表情符号应用自定义字体",
    "piko_newx_font_added": "字体添加成功",
    "piko_newx_font_add_failed": "字体添加失败",
    "piko_newx_font_deleted": "字体删除成功",
    "piko_newx_font_delete_failed": "字体删除失败",
    "piko_newx_font_invalid": "请确保字体为 .ttf 或 .otf 格式",
    "piko_newx_font_not_found": "未找到可删除的自定义字体",
    # Posts and media
    "piko_newx_post_options_title": "要隐藏的帖子菜单项",
    "piko_newx_post_options_summary": "选择要从 NewX 帖子菜单中隐藏的项目",
    "piko_newx_post_option_add_to_list": "添加到列表",
    "piko_newx_post_option_block": "屏蔽",
    "piko_newx_post_option_bookmark": "书签",
    "piko_newx_post_option_boost": "推广",
    "piko_newx_post_option_change_reply_permission": "更改回复权限",
    "piko_newx_post_option_community_note": "社群附注",
    "piko_newx_post_option_copy_link": "复制链接",
    "piko_newx_post_option_delete": "删除",
    "piko_newx_post_option_dislike": "不喜欢",
    "piko_newx_post_option_edit": "编辑",
    "piko_newx_post_option_follow": "关注",
    "piko_newx_post_option_highlight": "高亮",
    "piko_newx_post_option_like": "点赞",
    "piko_newx_post_option_mute": "屏蔽",
    "piko_newx_post_option_mute_conversation": "屏蔽对话",
    "piko_newx_post_option_not_interested": "不感兴趣",
    "piko_newx_post_option_pin": "置顶",
    "piko_newx_post_option_quote": "引用",
    "piko_newx_post_option_report": "举报",
    "piko_newx_post_option_repost": "转帖",
    "piko_newx_post_option_share": "分享帖子",
    "piko_newx_post_option_share_via_dm": "通过私信分享",
    "piko_newx_post_option_view_analytics": "查看分析",
    "piko_newx_post_option_view_hidden_replies": "查看隐藏回复",
    "piko_newx_post_option_view_interactions": "查看帖子互动",
    # Inline actions
    "piko_newx_inline_actions_title": "要隐藏的内联操作",
    "piko_newx_inline_actions_summary": "选择要从 NewX 帖子下方隐藏的操作",
    "piko_newx_inline_action_bookmark": "书签",
    "piko_newx_inline_action_dislike": "不喜欢",
    "piko_newx_inline_action_like": "点赞",
    "piko_newx_inline_action_reply": "回复",
    "piko_newx_inline_action_repost": "转帖",
    "piko_newx_inline_action_share": "分享",
    "piko_newx_inline_action_view_count": "查看次数",
    # Inline download
    "piko_newx_group_inline_download_title": "内联下载",
    "piko_newx_group_inline_download_summary": "自定义内联媒体下载选择器",
    "piko_newx_inline_download_button_title": "显示内联下载按钮",
    "piko_newx_inline_download_button_summary": "在 NewX 帖子下方直接添加下载按钮",
    "piko_newx_inline_download_hide_no_media_title": "无媒体时隐藏按钮",
    "piko_newx_inline_download_hide_no_media_summary": "仅在含有可下载媒体的帖子上显示内联下载按钮",
    "piko_newx_inline_download_options_title": "下载选项",
    "piko_newx_inline_download_options_summary": "选择下载文件的保存位置和命名方式",
    "piko_newx_inline_download_filename_template_title": "文件名模板",
    "piko_newx_inline_download_filename_template_summary": "从帖子数据生成保存文件名。点击编辑，可实时预览结果。",
    "piko_newx_inline_download_conflict_title": "媒体已存在时",
    "piko_newx_inline_download_conflict_summary": "重新下载已有媒体的帖子时的处理方式",
    "piko_newx_inline_download_conflict_overwrite": "覆盖已有文件",
    "piko_newx_inline_download_conflict_rename": "以新文件名保存",
    "piko_newx_inline_download_conflict_skip": "跳过已下载的媒体",
    "piko_newx_inline_download_images_tree_uri_title": "图片下载文件夹",
    "piko_newx_inline_download_images_tree_uri_summary": "为下载的图片选择的文件夹",
    "piko_newx_inline_download_images_display_path_title": "图片下载文件夹路径",
    "piko_newx_inline_download_images_display_path_summary": "图片下载文件夹的可读路径",
    "piko_newx_inline_download_videos_tree_uri_title": "视频下载文件夹",
    "piko_newx_inline_download_videos_tree_uri_summary": "为下载的视频选择的文件夹",
    "piko_newx_inline_download_videos_display_path_title": "视频下载文件夹路径",
    "piko_newx_inline_download_videos_display_path_summary": "视频下载文件夹的可读路径",
    # Media picker
    "piko_newx_media_picker_thumbnails_title": "加载媒体缩略图",
    "piko_newx_media_picker_thumbnails_summary": "在下载媒体选择器中加载图片预览，而非媒体类型图标",
    "piko_newx_media_picker_copy_link_title": "显示复制链接按钮",
    "piko_newx_media_picker_copy_link_summary": "在下载媒体选择器中显示用于复制媒体 URL 的按钮",
    "piko_newx_media_picker_merge_button_title": "显示合并按钮",
    "piko_newx_media_picker_merge_button_summary": "在媒体选择器中显示用于下载并合并分割的封面图的按钮",
    # Media tab
    "piko_newx_media_tab_default_title": "默认媒体标签",
    "piko_newx_media_tab_default_summary": "打开个人资料媒体标签时显示的默认子标签",
    "piko_newx_media_tab_photos": "照片",
    "piko_newx_media_tab_videos": "视频",
    # Reply sorting
    "piko_newx_group_reply_sorting_title": "回复排序",
    "piko_newx_group_reply_sorting_summary": "自定义帖子详情中回复的排序方式",
    "piko_newx_default_reply_sorting_title": "默认回复排序",
    "piko_newx_default_reply_sorting_summary": "帖子详情的默认回复排序方式（相关性、最新或最多点赞）",
    "piko_newx_remember_reply_sorting_title": "记住上次回复排序",
    "piko_newx_remember_reply_sorting_summary": "使用上次选择的回复排序方式，而非默认值",
    "piko_newx_reply_sort_relevance": "相关回复",
    "piko_newx_reply_sort_recency": "最新回复",
    "piko_newx_reply_sort_likes": "最多点赞回复",
    # For You filtering
    "piko_newx_group_for_you_filtering_title": "推荐过滤",
    "piko_newx_group_for_you_filtering_summary": "自定义话题过滤和\"为你推荐\"标签选择器",
    # Download (legacy)
    "piko_newx_download_filename_title": "文件名模板",
    "piko_newx_download_filename_tokens": "占位符",
    "piko_newx_download_filename_error_empty": "请输入文件名模板",
    "piko_newx_download_filename_error_static": "请添加 {id} 或 {timestamp} 以防止不同帖子相互覆盖",
    "piko_newx_download_filename_error_unclosed": "有一个大括号未关闭",
    "piko_newx_download_filename_error_unknown": "未知占位符 {%1$s}",
    "piko_newx_download_first_run_title": "选择下载文件夹",
    "piko_newx_download_first_run_both": "图片和视频在下载前各需要一个文件夹。",
    "piko_newx_download_first_run_images": "下载的图片需要一个文件夹。请选择一个便于查找的保存位置。",
    "piko_newx_download_first_run_images_action": "选择图片文件夹",
    "piko_newx_download_first_run_videos": "下载的视频需要一个文件夹。请选择一个便于查找的保存位置。",
    "piko_newx_download_first_run_videos_action": "选择视频文件夹",
    "piko_newx_download_first_run_retry": "设置文件夹后请再次点击下载。",
    "piko_newx_download_options_folders": "文件夹",
    "piko_newx_download_options_folder_hint": "文件将直接写入您选择的文件夹。选择 Pictures 或 DCIM 下的文件夹可让下载内容出现在相册中。",
    "piko_newx_download_options_folder_images": "图片",
    "piko_newx_download_options_folder_videos": "视频",
    "piko_newx_download_options_folder_not_set": "未设置 — 点击选择",
    "piko_newx_download_options_folder_denied": "点击重新授权",
    "piko_newx_download_options_filename_hint": "点击占位符以插入。大括号外的字符将原样保留。",
    "piko_newx_download_options_filename_preview": "预览：%1$s",
    "piko_newx_download_options_filename_reset": "恢复默认",
    "piko_newx_download_options_changed": "下载文件夹已更新",
    "piko_newx_download_options_cancelled": "未选择文件夹",
    # Custom sharing domain
    "piko_newx_custom_sharing_domain_title": "自定义分享域名",
    "piko_newx_custom_sharing_domain_summary": "分享帖子时将 x.com 替换为自定义域名（如 fxtwitter.com）",
    "piko_newx_custom_sharing_domain_invalid": "自定义分享域名格式不正确",
    # Share image
    "piko_newx_share_image_title": "将帖子分享为图片",
    "piko_newx_share_image_summary": "在帖子菜单中添加渲染图片分享操作",
    # Canonical URLs
    "piko_newx_canonical_urls_title": "使用规范 URL",
    "piko_newx_canonical_urls_summary": "在帖子和主页中显示展开的 URL 名称，并直接打开而非短网址 t.co",
    # Navigation
    "piko_newx_nav_editor_title": "导航栏",
    "piko_newx_nav_editor_summary": "为 NewX 底部导航栏选择最多五个目的地",
    "piko_newx_nav_editor_hint": "在各区域间拖动目的地。靠近顶部或底部时自动滚动。更改将在应用重启后生效。",
    "piko_newx_nav_editor_drag": "拖动以移动",
    "piko_newx_nav_editor_available": "可用目的地",
    "piko_newx_nav_editor_shown": "显示在导航栏中（最多 5 个）",
    "piko_newx_nav_editor_restart": "重启应用以应用更改",
    "piko_newx_nav_editor_restart_title": "重启应用？",
    "piko_newx_nav_editor_restart_message": "导航栏更改将在应用重启后生效。",
    "piko_newx_nav_editor_restart_confirm": "重启",
    "piko_newx_nav_bar_home": "主页",
    "piko_newx_nav_bar_explore": "探索",
    "piko_newx_nav_bar_notifications": "通知",
    "piko_newx_nav_bar_dm": "私信",
    "piko_newx_nav_bar_grok": "Grok",
    # Drawer
    "piko_newx_drawer_title": "要隐藏的抽屉项目",
    "piko_newx_drawer_summary": "选择要从 NewX 导航抽屉中隐藏的项目",
    "piko_newx_drawer_editor_title": "抽屉",
    "piko_newx_drawer_editor_summary": "选择要在 NewX 导航抽屉中显示的项目",
    "piko_newx_drawer_editor_hint": "切换将在下次打开抽屉时生效。重启应用可立即应用更改。",
    "piko_newx_drawer_editor_items": "抽屉项目",
    "piko_newx_drawer_editor_shortcuts": "快捷方式",
    "piko_newx_drawer_editor_restart": "重启应用以应用更改",
    "piko_newx_drawer_editor_restart_title": "重启应用？",
    "piko_newx_drawer_editor_restart_message": "抽屉更改将在应用重启后生效。",
    "piko_newx_drawer_editor_restart_confirm": "重启",
    "piko_newx_drawer_grok": "Grok",
    "piko_newx_drawer_theme_toggle": "主题切换",
    "piko_newx_show_grok_in_drawer_title": "在抽屉中显示 Grok",
    "piko_newx_show_grok_in_drawer_summary": "在 NewX 抽屉的个人资料下方添加 Grok 快捷方式",
    "piko_newx_show_messages_in_drawer_title": "在抽屉中显示私信",
    "piko_newx_show_messages_in_drawer_summary": "在 NewX 抽屉的个人资料下方添加私信快捷方式",
    "piko_newx_show_notifications_in_drawer_title": "在抽屉中显示通知",
    "piko_newx_show_notifications_in_drawer_summary": "在 NewX 抽屉的个人资料下方添加通知快捷方式",
    "piko_newx_show_piko_settings_in_drawer_title": "在抽屉底栏显示 Piko 设置",
    "piko_newx_show_piko_settings_in_drawer_summary": "在 NewX 抽屉底栏添加 Piko 设置快捷方式",
    # Gallery / cache
    "piko_newx_gallery_profile_photos_title": "照片标签的画廊布局",
    "piko_newx_gallery_profile_photos_summary": "将个人资料照片时间线替换为三列媒体画廊",
    "piko_newx_gallery_cache_stats_title": "媒体缓存统计",
    "piko_newx_gallery_cache_stats_summary": "查看缩略图磁盘使用量、会话命中率并清除缓存",
    "piko_newx_gallery_cache_clear_title": "清除媒体缓存？",
    "piko_newx_gallery_cache_clear": "清除缓存",
    "piko_newx_gallery_cache_clear_message": "移除所有已缓存的缩略图。下次访问时将从网络重新加载。",
    "piko_newx_gallery_cache_cleared": "已清除 %1$d 个缓存文件。",
    "piko_newx_gallery_cache_empty": "缓存为空。",
    "piko_newx_gallery_cache_loading": "正在加载缓存统计……",
    "piko_newx_gallery_cache_refresh": "刷新",
    "piko_newx_gallery_cache_disk_title": "磁盘缓存",
    "piko_newx_gallery_cache_limits_title": "限制",
    "piko_newx_gallery_cache_limits": "磁盘限制 %1$s · 条目限制 %2$s · 响应上限 %3$s",
    "piko_newx_gallery_cache_usage": "%1$s / %2$s（%3$d%%）",
    "piko_newx_gallery_cache_entries": "%1$d 个条目",
    "piko_newx_gallery_cache_session_title": "本次会话",
    "piko_newx_gallery_cache_hits_memory": "扩展内存命中：%1$d",
    "piko_newx_gallery_cache_hits_disk": "磁盘命中：%1$d",
    "piko_newx_gallery_cache_hits_loader": "应用图片加载器命中：%1$d",
    "piko_newx_gallery_cache_network": "网络：%1$d 已加载（%2$s），%3$d 失败",
    "piko_newx_gallery_cache_persisted": "已持久化：%1$d · 超大跳过：%2$d",
    "piko_newx_gallery_cache_evicted": "已回收：%1$d 个条目（回收 %2$s）",
    "piko_newx_gallery_cache_memory": "内存缓存：%1$d / %2$d KB",
    "piko_newx_gallery_cache_largest": "最大条目：%1$s",
    "piko_newx_gallery_cache_newest": "最新条目：%1$s",
    "piko_newx_gallery_cache_oldest": "最旧条目：%1$s",
    "piko_newx_gallery_cache_tmp": "%1$d 个临时文件待清理",
    "piko_newx_gallery_cache_failed": "无法读取媒体缓存。",
    # Force quality
    "piko_newx_force_highest_video_quality_title": "强制最高画质音视频",
    "piko_newx_force_highest_video_quality_summary": "以最高可用流媒体质量播放视频和音频，不受自适应降质或网络比特率限制影响",
    # Backup and restore
    "piko_newx_backup_restore_title": "备份和恢复",
    "piko_newx_backup_restore_summary": "保存或恢复 Piko NewX 设置",
    "piko_newx_backup_restore_no_file": "未选择设置文件",
    "piko_newx_backup_title": "备份设置",
    "piko_newx_backup_summary": "将 Piko NewX 设置保存为 JSON 文件",
    "piko_newx_backup_success": "NewX 设置已备份",
    "piko_newx_backup_failed": "无法备份 NewX 设置",
    "piko_newx_restore_title": "恢复设置",
    "piko_newx_restore_summary": "从 JSON 文件恢复 Piko NewX 设置",
    "piko_newx_restore_failed": "无法恢复 NewX 设置",
    # Scroll position
    "piko_newx_restore_profile_position_title": "恢复个人资料滚动位置",
    "piko_newx_restore_profile_position_summary": "按个人资料恢复每个标签页的保存位置",
    # Compose blur
    "piko_newx_disable_blur_title": "禁用 Compose 模糊",
    "piko_newx_disable_blur_summary": "移除 NewX Compose UI 的模糊效果，同时保留已配置的背景色调和遮罩效果",
    # Video scrolling
    "piko_newx_disable_video_scrolling_title": "禁用视频播放器滚动",
    "piko_newx_disable_video_scrolling_summary": "防止在 NewX 播放器中垂直滑动切换到下一个视频",
    # Logging
    "piko_newx_logging_title": "启用日志记录",
    "piko_newx_logging_summary": "将 NewX 诊断消息写入应用日志",
    # Server logging
    "piko_newx_server_logging_title": "捕获服务器错误",
    "piko_newx_server_logging_summary": "将解析后的 NewX 服务器错误保留在内存中，直到导出",
    "piko_newx_save_server_logs_title": "保存服务器日志",
    "piko_newx_save_server_logs_summary": "将捕获的服务器错误导出到 Download/piko-server-logs.txt",
    "piko_newx_server_logs_saved": "服务器日志已保存到 Download/piko-server-logs.txt",
    "piko_newx_server_logs_save_failed": "无法保存 NewX 服务器日志",
    # Feature switches
    "piko_newx_feature_switches_title": "功能开关",
    "piko_newx_feature_switches_summary": "管理、导入或导出功能开关覆盖值",
    "piko_newx_feature_switch_manage_title": "管理功能开关",
    "piko_newx_feature_switch_manage_summary": "搜索已观察到的开关并覆盖布尔、数字、字符串或列表值",
    "piko_newx_feature_switch_search_hint": "搜索功能开关",
    "piko_newx_feature_switch_no_results": "没有匹配的功能开关",
    "piko_newx_feature_switch_empty": "尚未观察到任何功能开关。使用 X 后返回此页面。",
    "piko_newx_feature_switch_not_overridden_section": "默认",
    "piko_newx_feature_switch_overridden_section": "已覆盖",
    "piko_newx_feature_switch_add_title": "添加功能开关",
    "piko_newx_feature_switch_add": "添加功能开关",
    "piko_newx_feature_switch_edit_title": "编辑功能开关",
    "piko_newx_feature_switch_key_hint": "功能开关键",
    "piko_newx_feature_switch_value_type": "值类型",
    "piko_newx_feature_switch_boolean_value": "布尔值",
    "piko_newx_feature_switch_number_value": "数字值",
    "piko_newx_feature_switch_string_value": "字符串值",
    "piko_newx_feature_switch_list_value": "列表值，每行一个",
    "piko_newx_feature_switch_null": "null",
    "piko_newx_feature_switch_type_boolean": "布尔",
    "piko_newx_feature_switch_type_int": "整数",
    "piko_newx_feature_switch_type_long": "长整数",
    "piko_newx_feature_switch_type_float": "单精度浮点",
    "piko_newx_feature_switch_type_double": "双精度浮点",
    "piko_newx_feature_switch_type_string": "字符串",
    "piko_newx_feature_switch_type_list": "列表",
    "piko_newx_feature_switch_next": "下一步",
    "piko_newx_feature_switch_save": "保存",
    "piko_newx_feature_switch_cancel": "取消",
    "piko_newx_feature_switch_remove": "移除覆盖",
    "piko_newx_feature_switch_invalid_key": "请输入功能开关键。",
    "piko_newx_feature_switch_invalid_value": "请输入此开关类型的有效值。",
    "piko_newx_feature_switch_duplicate_key": "该功能开关已存在。",
    "piko_newx_feature_switch_export_title": "导出功能开关",
    "piko_newx_feature_switch_export_summary": "将当前功能开关覆盖值保存为 JSON 文件",
    "piko_newx_feature_switch_export_success": "功能开关已导出",
    "piko_newx_feature_switch_export_failed": "无法导出功能开关",
    "piko_newx_feature_switch_import_title": "导入功能开关",
    "piko_newx_feature_switch_import_summary": "从 JSON 文件替换当前功能开关覆盖值",
    "piko_newx_feature_switch_import_success": "功能开关已导入",
    "piko_newx_feature_switch_import_failed": "无法导入功能开关",
    "piko_newx_feature_switch_file_not_selected": "未选择功能开关文件",
    # Crash tools
    "piko_newx_group_debug_tools_title": "开发者工具",
    "piko_newx_group_debug_tools_summary": "从帖子菜单中查看 NewX 内部数据",
    "piko_newx_crash_app_title": "崩溃应用",
    "piko_newx_crash_app_summary": "立即崩溃应用以测试崩溃日志",
    "piko_newx_crash_post_option_title": "帖子菜单崩溃项",
    "piko_newx_crash_post_option_summary": "在时间线帖子菜单中添加崩溃选项",
    # Browse tweet object
    "piko_newx_browse_tweet_object_title": "浏览推文对象",
    "piko_newx_browse_tweet_object_summary": "在帖子菜单中添加调试选项以检查推文对象",
    # Dynamic colors group
    "piko_newx_group_dynamic_colors_title": "动态取色",
    "piko_newx_group_dynamic_colors_summary": "自定义 Material You 配色和主题强调色行为",
    # Profile post sort
    "piko_newx_profile_post_sort_default_title": "默认个人资料帖子排序",
    "piko_newx_profile_post_sort_default_summary": "打开个人资料帖子时的默认排序方式（最新或最热）",
    "piko_newx_profile_post_sort_latest": "最新",
    "piko_newx_profile_post_sort_popular": "最热",
}

# ── Morphe import/export strings (newx) ─────────────────────────────────────
MORPHE_ZH: dict[str, str] = {
    "morphe_settings_import_failure_parse": "无法恢复 NewX 设置：%1$s",
    "morphe_settings_import_reset": "NewX 设置已重置为默认值",
    "morphe_settings_import_success": "已恢复 %1$d 项 NewX 设置",
}


def _read_xml_keys(content: str) -> dict[str, str]:
    """Extract name→value pairs from an Android strings.xml."""
    result: dict[str, str] = {}
    for m in re.finditer(
        r'<string\s+name="([^"]+)"[^>]*>(.*?)</string>', content, re.DOTALL
    ):
        result[m.group(1)] = m.group(2)
    return result


def _build_strings_xml(
    keys: dict[str, str],
    translations: dict[str, str],
    *,
    fallback: dict[str, str] | None = None,
) -> str:
    """Build a complete zh-rCN strings.xml merging translations with upstream values."""
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<resources>",
    ]
    for key, en_value in keys.items():
        if key in translations:
            value = translations[key]
        elif fallback and key in fallback:
            value = fallback[key]
        else:
            # Untranslated – use English as placeholder (better than missing)
            value = en_value
        # Escape XML special characters in value
        value = (
            value.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        lines.append(f'    <string name="{key}">{value}</string>')
    lines.append("</resources>")
    return "\n".join(lines) + "\n"


def localize_piko_settings(
    piko_directory: Path,
    cached_en_twitter: str | None = None,
    cached_en_newx: str | None = None,
) -> None:
    """
    Create zh-rCN resource files in the temporary Piko build directory.

    Must be called AFTER pre_build_cleanup() (which deletes upstream zh-rCN/twitter)
    and BEFORE gradlew buildAndroid.

    Since pre_build_cleanup() removes values/twitter/, the English source content
    must be passed via cached_en_twitter / cached_en_newx (read before cleanup).
    If not provided, falls back to reading from disk (for testing against uncleaned repos).
    """
    addresources = piko_directory / "patches" / "src" / "main" / "resources" / "addresources"

    # English source keys (use cached content if available, otherwise read from disk)
    if cached_en_twitter is not None:
        en_twitter_keys = _read_xml_keys(cached_en_twitter)
    else:
        en_twitter_xml = addresources / "values" / "twitter" / "strings.xml"
        en_twitter_keys = _read_xml_keys(en_twitter_xml.read_text(encoding="utf-8"))

    if cached_en_newx is not None:
        en_newx_keys = _read_xml_keys(cached_en_newx)
    else:
        en_newx_xml = addresources / "values" / "newx" / "strings.xml"
        en_newx_keys = _read_xml_keys(en_newx_xml.read_text(encoding="utf-8"))

    # ── Create zh-rCN/twitter/strings.xml ──
    zh_twitter_dir = addresources / "values-zh-rCN" / "twitter"
    zh_twitter_dir.mkdir(parents=True, exist_ok=True)

    zh_twitter_xml = _build_strings_xml(en_twitter_keys, TWITTER_ZH)
    (zh_twitter_dir / "strings.xml").write_text(zh_twitter_xml, encoding="utf-8")

    # ── Create zh-rCN/newx/strings.xml ──
    zh_newx_dir = addresources / "values-zh-rCN" / "newx"
    zh_newx_dir.mkdir(parents=True, exist_ok=True)

    all_newx_translations = {**NEWX_ZH, **MORPHE_ZH}
    zh_newx_xml = _build_strings_xml(en_newx_keys, all_newx_translations)
    (zh_newx_dir / "strings.xml").write_text(zh_newx_xml, encoding="utf-8")

    # ── Statistics ──
    missing_twitter = sorted(set(en_twitter_keys) - set(TWITTER_ZH))
    missing_newx = sorted(
        set(en_newx_keys) - set(all_newx_translations)
    )

    print()
    print("Piko localization:")
    print(f"  English twitter strings: {len(en_twitter_keys)}")
    print(f"  Chinese twitter strings: {len(en_twitter_keys) - len(missing_twitter)}")
    print(f"  Missing Chinese twitter: {len(missing_twitter)}")
    print()
    print(f"  English newx strings:    {len(en_newx_keys)}")
    print(f"  Chinese newx strings:    {len(en_newx_keys) - len(missing_newx)}")
    print(f"  Missing Chinese newx:    {len(missing_newx)}")
    print()

    total_en = len(en_twitter_keys) + len(en_newx_keys)
    total_missing = len(missing_twitter) + len(missing_newx)
    print(f"  Total English:   {total_en}")
    print(f"  Total Chinese:   {total_en - total_missing}")
    print(f"  Total Missing:   {total_missing}")

    if total_missing > 0:
        print()
        print("  WARNING: The following keys have no zh-CN translation:")
        for k in missing_twitter:
            print(f"    [twitter] {k}")
        for k in missing_newx:
            print(f"    [newx]    {k}")
    else:
        print()
        print("  All strings translated [OK]")

    print()
