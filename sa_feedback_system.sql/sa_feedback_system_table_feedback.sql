
-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
CREATE TABLE IF NOT EXISTS `feedback` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `academic_year` varchar(10) NOT NULL,
  `current_year` varchar(4) NOT NULL,
  `department` varchar(70) NOT NULL,
  `course_name` varchar(70) NOT NULL,
  `event_name` varchar(70) NOT NULL,
  `form_time` varchar(12) NOT NULL,
  `form_status` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `academic_year`, `current_year`, `department`, `course_name`, `event_name`, `form_time`, `form_status`) VALUES
(3, '2022-2023', 'B.E.', 'Information Technology', 'Blockchain and Ledger Technology', 'BDLT Course Feedback', '1679760781', 0);
