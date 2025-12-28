<?php
// التوكن الخاص بك الذي أرسلته
$token = "8533745563:AAHfMIKAoEGcWB3p6NahYePP7HHeii3GWtc";
$api_url = "https://api.telegram.org/bot$token/";

$update = json_decode(file_get_contents("php://input"), TRUE);
$chat_id = $update["message"]["chat"]["id"];
$text = $update["message"]["text"];
$user_id = $update["message"]["from"]["id"];
$username = $update["message"]["from"]["username"];

// ملف تخزين البيانات
$db_file = "users.json";
if(!file_exists($db_file)) file_put_contents($db_file, json_encode([]));
$db = json_decode(file_get_contents($db_file), true);

if (!isset($db[$user_id])) {
    $db[$user_id] = ["points" => 0, "referred" => false];
}

// نظام الإحالة (الروابط)
if (strpos($text, "/start ") === 0) {
    $inviter_id = str_replace("/start ", "", $text);
    if ($inviter_id != $user_id && $db[$user_id]['referred'] == false) {
        $db[$inviter_id]['points'] += 1;
        $db[$user_id]['referred'] = true;
        sendMessage($inviter_id, "🔔 **New Referral!**\n🇷🇺 Новый пользователь зашел по вашей ссылке!\n💰 Points: " . $db[$inviter_id]['points']);
    }
}

file_put_contents($db_file, json_encode($db));

// رسالة الترحيب الاحترافية
if ($text == "/start" || strpos($text, "/start") === 0) {
    $welcome = "🛡️ **Welcome to Cyber Sentry DB**\n";
    $welcome .= "----------------------------\n";
    $welcome .= "🇺🇸 Send your email to check for data leaks.\n";
    $welcome .= "🇷🇺 Отправьте свой email, чтобы проверить утечку данных.\n\n";
    $welcome .= "👇 **Example / Пример:** `example@gmail.com`";
    sendMessage($chat_id, $welcome);
} 

// فحص الإيميل
elseif (filter_var($text, FILTER_VALIDATE_EMAIL)) {
    $points = $db[$user_id]['points'];
    $required = 3; // عدد الأشخاص المطلوب دعوتم
    
    if ($points < $required) {
        $bot_name = "CyberSentry_bot"; // تأكد من وضع يوزر بوتك هنا بدون @
        $ref_link = "https://t.me/$bot_name?start=$user_id";
        
        $msg = "⚠️ **ACCESS DENIED / ДОСТУП ЗАПРЕЩЕН**\n\n";
        $msg .= "🇺🇸 To see the leaked data, you must invite $required friends.\n";
        $msg .= "🇷🇺 Чтобы увидеть данные, вы должны пригласить $required друзей.\n\n";
        $msg .= "📊 Progress: ($points/$required)\n";
        $msg .= "🔗 Your Link: $ref_link";
        sendMessage($chat_id, $msg);
    } else {
        // نتيجة عشوائية احترافية
        $leaks = ["Database_v2_2024", "Private_Cloud_Dump", "Social_Network_Leak"];
        $src = $leaks[array_rand($leaks)];
        $res = "✅ **SCAN COMPLETE / СКАНИРОВАНИЕ ЗАВЕРШЕНО**\n\n";
        $res .= "📧: `$text`\n";
        $res .= "🛑 Status: **CRITICAL EXPOSURE**\n";
        $res .= "📂 Source: $src\n\n";
        $res .= "Please change your password immediately!";
        sendMessage($chat_id, $res);
    }
}

function sendMessage($chat_id, $text) {
    global $api_url;
    file_get_contents($api_url . "sendMessage?chat_id=$chat_id&text=" . urlencode($text) . "&parse_mode=Markdown");
}
?>
