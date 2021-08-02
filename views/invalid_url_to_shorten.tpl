<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="styles.css">
    <title>Invalid URL provided to shortener</title>

<style>
    .center_outer {
        margin: auto;
        width: 60%;
        border: 2px solid #5b34eb;
        padding: 10px;
    }

    .center_inner {
        text-align: center;
        font-size: larger;
        padding: 50px;
        font-family: arial, sans-serif;
    }

body {
  background-color: lightblue;
}

</style>

</head>
<body>
<div class="center_outer">
<div class="center_inner">
    Invalid URL string, can not shorten <b>"{{in_long_url}}"</b>.
    <br>
    <br>
    <a href= "{{try_again_url}}">Try Again</a>.
</div>
</div>
 </body>
</html>