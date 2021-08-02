<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="styles.css">
    <title>Create a new short URL</title>

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

<form action="/new" method="post">
            Enter the URL you'd like shortened: <input name="long_url" type="text" size="50"/>
            <input value="Submit" type="submit" />
        </form>
</div>
</div>

</body>
</html>
