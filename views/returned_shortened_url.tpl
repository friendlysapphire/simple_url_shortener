<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="styles.css">
    <title>Your new short URL</title>

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
    The short URL for <b>{{in_long_url}}</b> is:
    <br>
    <br>
    <a href="{{full_short_url}}">{{full_short_url}}</a>


</div>
</div>
 </body>
</html>