<!doctype html>
<html lang="en">

    <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="styles.css">
    <title>URL shortener stats and info page</title>

    <style>

    table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
    }

    td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
    }

    tr:nth-child(even) {
    background-color: #dddddd;
    }
    </style>

    </head>

     <body>
        <table style=background-color:#dddddd>
        <tr>
        <td> Host is live at: {{base_url}} </td>
        </tr>
        </table>
        <br>
        <br>
        <form action="/delete" method="post">

        <table>
            <tr>
            % for i in headings:
                <th>{{i}}</th>
            % end
            </tr>

            % for row in rows:
                <tr>
                % for i in row:
                    <td>
                    {{i}}
                    </td>
                % end
                <td>
                <button type="submit" name="delrow" value="{{row[0]}}">Delete</button>
                </td>
                </tr>
            % end
        </table>
    </body>
</html>