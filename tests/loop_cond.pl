$abc = 6
$abc++
/*
this is a multiline comment
yes
*/
$foo = 3 * 2 / 2 + 2
while($foo > 2){
  #this is a single line comment
  $var = "Variable inside while"
  print($foo++)
  if ($foo == 1){
    if($foo > 1){
      $varif = "Variable inside if"
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
