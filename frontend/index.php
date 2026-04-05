<!DOCTYPE html>
<html>
<head>
    <title>Passport Validator</title>

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
            width: 40%;
            margin: auto;
            margin-top: 80px;
        }

        button {
            padding: 10px 20px;
            background: #3b82f6;
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 5px;
        }

        img {
            margin-top: 10px;
            border-radius: 10px;
        }
    </style>
</head>

<body>

<div class="card">

<h2>Passport Photo Validation</h2>

<form action="result.php" method="POST" enctype="multipart/form-data">

    <input type="file" name="image" onchange="previewImage(event)" required>
    
    <br><br>

    <img id="preview" width="200"/>

    <br><br>

    <button type="submit">Validate</button>

</form>

</div>

<script>
function previewImage(event) {
    const img = document.getElementById('preview');
    img.src = URL.createObjectURL(event.target.files[0]);
}
</script>

</body>
</html>