<?php
$name = $_POST['intoducir_nombre'];
$mail = $_POST['introducir_email'];
$message = $_POST['introducir_mensaje'];

$header = 'From: ' . $mail . " \r\n";
$header .= "X-Mailer: PHP/" . phpversion() . " \r\n";
$header .= "Mime-Version: 1.0 \r\n";
$header .= "Content-Type: text/plain";

$message = "Este mensaje fue enviado por: " . $name . " \r\n";
$message .= "Su e-mail es: " . $mail . " \r\n";
$message .= "Mensaje: " . $_POST['message'] . " \r\n";
$message .= "Enviado el: " . date('d/m/Y', time());

$para = 'franciscolupica@gmail.com';
$asunto = 'Mensaje de Consulta 4us';

mail($para, $asunto, utf8_decode($message), $header);

header("Location:index.html");
?>
<!-- MADE BY LUPICA -->