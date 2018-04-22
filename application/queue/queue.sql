DROP TABLE IF EXISTS `queue`;
CREATE TABLE `queue` (
  `qid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `queue_type` char(20),
  `processed` int(1) DEFAULT 0,
  `hostname` char(20),
  `requestID` varchar(80),
  `parameter` varchar(1000),
  `pid` int(5) DEFAULT '0',
  `assign_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY (`qid`)
);
