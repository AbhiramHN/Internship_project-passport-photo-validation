<?php

$data = null;
$error = null;

if(isset($_FILES['image'])) {

    $file = $_FILES['image'];

    $cfile = new CURLFile($file['tmp_name'], $file['type'], $file['name']);

    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL, "http://127.0.0.1:5000/validate");
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, ['file' => $cfile]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);

    if(curl_errno($ch)) {
        $error = curl_error($ch);
    }

    curl_close($ch);

    $data = json_decode($response, true);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Result</title>

    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
        }

        .card {
            background: #1e293b;
            padding: 30px;
            border-radius: 10px;
            width: 50%;
            margin: auto;
            margin-top: 50px;
        }

        .valid { color: #22c55e; }
        .invalid { color: #ef4444; }

        ul { text-align: left; display:inline-block; }
    </style>
</head>

<body>

<div class="card">

<h2>Validation Result</h2>

<?php if($error): ?>
    <p style="color:red;">Error: <?= $error ?></p>

<?php elseif($data): ?>

    <!-- STATUS -->
    <?php if($data['status'] == "Valid"): ?>
        <h2 class="valid">Valid Passport Photo</h2>
    <?php else: ?>
        <h2 class="invalid">Invalid Passport Photo</h2>

        <?php if(!empty($data['reasons'])): ?>
            <h4>Reasons:</h4>
            <ul>
                <?php foreach($data['reasons'] as $reason): ?>
                    <li><?= $reason ?></li>
                <?php endforeach; ?>
            </ul>
        <?php endif; ?>
    <?php endif; ?>

    <br>

<?php else: ?>
    <p>No response from API</p>
<?php endif; ?>

<br><br>

<a href="index.php" style="color:lightblue;">⬅ Upload Another</a>

</div>

</body>
</html>