<?php
    //require the autoload php file
    require 'vendor/autoload.php';
    //create new mongodb client
    $client = new MongoDB\Client("mongodb://localhost:27017/");
    //seleect database
    $db = $client->{"yahoo-db"};
    //select the stocks collection
    $collection = $db->{"stocks"};
    //retrieve all the documents from the collection
    $result = $collection->find([]);

    //function to display stocks in a table
    function display_stocks($stocks){
        echo '<table border="1">';
            echo '<tr><th><a href="?sort=_id">Index</a></th><th><a href="?sort=Symbol">Symbol</a></th><th><a href="?sort=Name">Name</a></th><th><a href="?sort=Price">Price</a></th><th><a href="?sort=Change">Change</a></th><th><a href="?sort=Volume">Volume</a></th></tr>';
      
            foreach ($stocks as $stock) {
                echo '<tr>';
                    echo '<td>' . $stock['_id'] . '</td>';
                    echo '<td>' . $stock['Symbol'] . '</td>';
                    echo '<td>' . $stock['Name'] . '</td>';
                    echo '<td>' . $stock['Price'] . '</td>';
                    echo '<td>';
                    #display a + if stock increase is greater than 0
                    if ($stock['Change'] > 0) {
                        echo '+' . $stock['Change'] . '</td>';
                    }
                    else {echo $stock['Change'] . '</td>';}
                    echo '<td>' . $stock['Volume'] . '</td>';
                echo '</tr>';
            }
        echo '</table>';
    }

    if (isset($_GET['sort'])) 
    {
        $fields_s = $_GET['sort'];
        $array_s = $collection->find([], ['sort' => [$fields_s => 1]]);
        display_stocks($array_s);
    } else {
        #display all documents from the collection
        display_stocks($result);
    }
?>
