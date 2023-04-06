
-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
CREATE TABLE IF NOT EXISTS `courses` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `year` varchar(4) NOT NULL,
  `department` varchar(70) NOT NULL,
  `course_name` varchar(70) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `year`, `department`, `course_name`) VALUES
(1, 'B.E.', 'Information Technology', 'Blockchain and Ledger Technology'),
(2, 'F.E.', 'Computer Science', 'Engineering Mathematics-I'),
(3, 'S.E.', 'Civil Engineering', 'Mechanics of Solids'),
(4, 'T.E.', 'Electronics and Telecommunication', 'Digital Communication');
