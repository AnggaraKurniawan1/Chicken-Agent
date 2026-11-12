<?php
// Reverse proxy ke server Python Chicken-Agent (Port 5173)
$target = 'http://127.0.0.1:5173' . $_SERVER['REQUEST_URI'];

$ch = curl_init($target);
$method = $_SERVER['REQUEST_METHOD'];

curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HEADER, true);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

if ($method === 'POST') {
    $body = file_get_contents('php://input');
    curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
}

// Teruskan header
$headers = [];
if (function_exists('getallheaders')) {
    foreach (getallheaders() as $key => $val) {
        if (strtolower($key) !== 'host') {
            $headers[] = "$key: $val";
        }
    }
}
$headers[] = 'Host: 127.0.0.1:5173';
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_TIMEOUT, 120);

$response = curl_exec($ch);

if ($response === false) {
    http_response_code(502);
    echo '<!DOCTYPE html>
    <html lang="id">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Chicken-Agent | EnvKit</title>
      <style>
        body { font-family: system-ui, sans-serif; background: #0b0f19; color: #f8fafc; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 2.5rem; border-radius: 16px; border: 1px solid #334155; max-width: 500px; text-align: center; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }
        h1 { color: #f59e0b; margin-top: 0; font-size: 1.8rem; }
        p { color: #94a3b8; line-height: 1.6; font-size: 1rem; }
        code { background: #0f172a; padding: 0.2rem 0.5rem; border-radius: 6px; color: #38bdf8; font-family: monospace; }
        .status-badge { display: inline-block; padding: 0.35rem 0.8rem; background: #ef444422; color: #ef4444; border: 1px solid #ef444455; border-radius: 9999px; font-weight: 600; font-size: 0.85rem; margin-bottom: 1rem; }
      </style>
    </head>
    <body>
      <div class="card">
        <div class="status-badge">● Server Offline</div>
        <h1>🐔 Chicken-Agent Dev Server</h1>
        <p>Server web Python Chicken-Agent belum aktif di port <code>5173</code>.</p>
        <p>Jalankan server melalui tombol <b>Start dev</b> di dashboard EnvKit atau double click <code>start_web.bat</code> di folder proyek.</p>
      </div>
    </body>
    </html>';
    curl_close($ch);
    exit;
}

$header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
$resp_header = substr($response, 0, $header_size);
$resp_body = substr($response, $header_size);
$status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);

http_response_code($status_code);

foreach (explode("\r\n", $resp_header) as $hdr) {
    if ($hdr && !preg_match('/^Transfer-Encoding:/i', $hdr) && !preg_match('/^Content-Length:/i', $hdr)) {
        header($hdr, false);
    }
}

echo $resp_body;
curl_close($ch);
