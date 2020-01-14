<?php

date_default_timezone_set('America/Sao_Paulo');
$aRet = array();

$hostname = 'localhost';
$username = 'root';
$password = 'destino2002';
$database = 'send';
 
try {
    $pdo = new PDO("mysql:host=$hostname;dbname=$database;charset=utf8", $username, $password,
    array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES utf8"));
    
    switch($_REQUEST['action']){
		case "saveStatus":
			$queryresposta="UPDATE envios SET status = '{$_REQUEST['status']}' where id IN ({$_REQUEST['id']})";
			$stmt = $pdo->prepare($queryresposta);
			$stmt->execute();
			$aRet = [
				'success'=>true,
				'message'=>"Status salvo com sucesso"
			];
			break;
		default:
			$queryresposta="SELECT * from envios where status = 0";
			$stmt = $pdo->prepare($queryresposta);
			$stmt->execute();
			$aRet = $stmt->fetchAll(PDO::FETCH_ASSOC);
			$aIds = [];
			foreach ($aRet AS $row){
				$aIds[] = $row['id'];
			}
			
			$queryresposta="UPDATE envios SET status = 1 where id IN (".implode(",",$aIds).")";
			$stmt = $pdo->prepare($queryresposta);
			$stmt->execute();
			break;
		
	}
    
}
catch(PDOException $e){
    
}
header('content-type: application/json; charset=utf-8');
echo json_encode($aRet);
