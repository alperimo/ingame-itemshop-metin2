
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for nesnemarket
-- ----------------------------
DROP TABLE IF EXISTS `nesnemarket`;
CREATE TABLE `nesnemarket` (
  `id` int(10) unsigned DEFAULT NULL,
  `account_id` int(10) unsigned DEFAULT NULL,
  `login` varchar(10) DEFAULT NULL,
  `vnum` int(10) unsigned DEFAULT NULL,
  `kristal` int(10) unsigned DEFAULT NULL,
  `adet` int(10) unsigned DEFAULT NULL,
  `item_sure` int(10) unsigned DEFAULT NULL,
  `item_id` int(10) unsigned DEFAULT NULL,
  `tarih` varchar(30) NOT NULL DEFAULT ''
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

