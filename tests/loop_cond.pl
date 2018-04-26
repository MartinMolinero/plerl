$abc = 6
$abc--
/*
this is a multiline comment
yes
*/
$foo = 0 
while($foo > 2){
  #this is a single line comment
  print($foo++)
  if ($foo == 1){
    if($foo > 1){
      print($foo)
    }
    else{
      print($foo)
    }
  }else{
    print($foo)
  }
  $foo--
}
