# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

## 2.1. Tổng quan về Big Data

### 2.1.1. Khái niệm Big Data

Trong thời đại công nghệ số hiện nay, lượng dữ liệu được tạo ra mỗi ngày đang tăng lên với tốc độ chóng mặt. Theo thống kê, mỗi ngày có khoảng 2.5 quintillion bytes dữ liệu được tạo ra từ các nguồn khác nhau như mạng xã hội, thiết bị IoT, giao dịch trực tuyến và nhiều nguồn khác. Sự bùng nổ dữ liệu này đã dẫn đến sự ra đời của khái niệm Big Data hay còn gọi là Dữ liệu lớn.

Big Data là thuật ngữ dùng để mô tả các tập dữ liệu có khối lượng cực kỳ lớn, phức tạp và đa dạng mà các công cụ xử lý dữ liệu truyền thống không thể xử lý một cách hiệu quả. Khái niệm Big Data không chỉ đơn thuần đề cập đến kích thước của dữ liệu mà còn bao gồm toàn bộ quá trình thu thập, lưu trữ, quản lý, xử lý và phân tích dữ liệu để trích xuất ra những thông tin có giá trị phục vụ cho việc ra quyết định trong kinh doanh, nghiên cứu khoa học và nhiều lĩnh vực khác.

Sự khác biệt cơ bản giữa Big Data và dữ liệu truyền thống nằm ở quy mô và độ phức tạp. Trong khi dữ liệu truyền thống có thể được xử lý bằng các công cụ như Excel, SQL Server hay các hệ quản trị cơ sở dữ liệu quan hệ thông thường, thì Big Data đòi hỏi các công nghệ và kiến trúc đặc biệt được thiết kế riêng để xử lý khối lượng dữ liệu khổng lồ một cách hiệu quả. Các công nghệ này bao gồm hệ thống file phân tán như HDFS, các framework xử lý song song như Apache Spark, và các cơ sở dữ liệu NoSQL như MongoDB hay Cassandra.

### 2.1.2. Đặc trưng 5V của Big Data

Để hiểu rõ hơn về bản chất của Big Data, các nhà nghiên cứu đã đưa ra mô hình 5V để mô tả các đặc trưng cơ bản của dữ liệu lớn. Mô hình này ban đầu chỉ có 3V được đề xuất bởi Doug Laney vào năm 2001, sau đó được mở rộng thành 5V để phản ánh đầy đủ hơn các khía cạnh của Big Data.

Đặc trưng đầu tiên là Volume (Khối lượng), đề cập đến lượng dữ liệu khổng lồ cần được lưu trữ và xử lý. Khối lượng dữ liệu trong Big Data thường được đo bằng đơn vị terabytes (TB), petabytes (PB) hoặc thậm chí exabytes (EB). Ví dụ điển hình là Facebook lưu trữ hơn 300 petabytes dữ liệu người dùng, hay Google xử lý hơn 20 petabytes dữ liệu mỗi ngày. Trong bối cảnh đồ án này, dataset CIFAKE với 120,000 ảnh tuy không quá lớn về mặt dung lượng nhưng đủ để minh họa cho việc cần thiết phải sử dụng các công nghệ Big Data để xử lý hiệu quả.

Đặc trưng thứ hai là Velocity (Tốc độ), mô tả tốc độ mà dữ liệu được tạo ra, thu thập và cần được xử lý. Trong nhiều ứng dụng hiện đại, dữ liệu đến liên tục theo thời gian thực và cần được xử lý ngay lập tức để đưa ra quyết định kịp thời. Ví dụ như hệ thống phát hiện gian lận thẻ tín dụng cần phân tích giao dịch trong vài mili giây, hay hệ thống giám sát mạng xã hội cần theo dõi hàng triệu bài đăng mỗi phút. Tốc độ xử lý nhanh là yếu tố then chốt để tạo ra giá trị từ dữ liệu.

Đặc trưng thứ ba là Variety (Đa dạng), phản ánh sự đa dạng về loại hình và định dạng của dữ liệu. Big Data không chỉ bao gồm dữ liệu có cấu trúc như bảng biểu trong cơ sở dữ liệu quan hệ, mà còn bao gồm dữ liệu bán cấu trúc như JSON, XML và dữ liệu phi cấu trúc như văn bản, hình ảnh, video, âm thanh. Trong đồ án này, dữ liệu đầu vào là các file ảnh định dạng JPG, thuộc loại dữ liệu phi cấu trúc, cần được chuyển đổi thành dạng vector số để có thể áp dụng các thuật toán machine learning.

Đặc trưng thứ tư là Veracity (Độ tin cậy), đề cập đến chất lượng và độ chính xác của dữ liệu. Không phải tất cả dữ liệu đều đáng tin cậy, dữ liệu có thể chứa nhiễu, thiếu sót, không nhất quán hoặc thậm chí sai lệch. Việc đảm bảo chất lượng dữ liệu là một thách thức lớn trong Big Data, đòi hỏi các quy trình làm sạch và xác thực dữ liệu nghiêm ngặt. Trong bài toán phát hiện ảnh Deepfake, độ tin cậy của nhãn dữ liệu (REAL hay FAKE) là yếu tố quan trọng ảnh hưởng đến chất lượng của mô hình.

Đặc trưng cuối cùng là Value (Giá trị), thể hiện khả năng trích xuất thông tin có ý nghĩa và giá trị từ dữ liệu. Mục đích cuối cùng của việc thu thập và xử lý Big Data là để tạo ra giá trị, có thể là insights kinh doanh, dự đoán xu hướng, phát hiện bất thường hay hỗ trợ ra quyết định. Giá trị của Big Data không nằm ở bản thân dữ liệu mà nằm ở những gì chúng ta có thể học được từ dữ liệu đó.

### 2.1.3. Vai trò của Big Data trong xử lý dữ liệu lớn

Big Data đóng vai trò then chốt trong việc giải quyết các bài toán xử lý dữ liệu quy mô lớn mà các phương pháp truyền thống không thể đáp ứng được. Vai trò quan trọng nhất của Big Data là khả năng lưu trữ phân tán, cho phép phân chia dữ liệu lớn thành nhiều phần nhỏ hơn và lưu trữ trên nhiều máy tính khác nhau trong một cụm (cluster). Cách tiếp cận này giúp vượt qua giới hạn về dung lượng lưu trữ của một máy đơn lẻ và tăng khả năng mở rộng của hệ thống.

Bên cạnh đó, Big Data cho phép xử lý song song, nghĩa là nhiều máy tính trong cụm có thể đồng thời xử lý các phần dữ liệu khác nhau. Điều này giúp tăng đáng kể tốc độ xử lý so với việc xử lý tuần tự trên một máy. Ví dụ, nếu một máy cần 10 giờ để xử lý một tập dữ liệu, thì với 10 máy xử lý song song, thời gian có thể giảm xuống còn khoảng 1 giờ (trong điều kiện lý tưởng).

Khả năng mở rộng (scalability) là một ưu điểm quan trọng khác của Big Data. Khi lượng dữ liệu tăng lên, hệ thống có thể dễ dàng mở rộng bằng cách thêm các máy mới vào cụm mà không cần thay đổi kiến trúc hay viết lại code. Đây là mô hình scale-out, khác với mô hình scale-up truyền thống là nâng cấp phần cứng của một máy đơn lẻ.

Cuối cùng, các hệ thống Big Data được thiết kế với khả năng chịu lỗi (fault tolerance) cao. Khi một hoặc một số máy trong cụm gặp sự cố, hệ thống vẫn tiếp tục hoạt động bình thường nhờ cơ chế sao lưu dữ liệu và phân phối lại công việc. Điều này đảm bảo tính sẵn sàng và độ tin cậy của hệ thống trong môi trường sản xuất.

Trong bối cảnh đồ án này, việc xử lý 120,000 ảnh từ dataset CIFAKE đặt ra những thách thức đáng kể nếu sử dụng phương pháp truyền thống. Nếu dùng Python thông thường với vòng lặp for để duyệt qua từng ảnh, quá trình xử lý sẽ diễn ra tuần tự, chỉ sử dụng một CPU core tại một thời điểm, dẫn đến thời gian xử lý kéo dài hàng giờ. Ngoài ra, việc load toàn bộ ảnh vào bộ nhớ RAM cũng có thể gây ra vấn đề về tài nguyên. Với việc áp dụng các công nghệ Big Data như HDFS và Apache Spark, dữ liệu được phân tán trên nhiều node, xử lý song song trên nhiều Worker, và hệ thống tự động cân bằng tải cũng như xử lý các trường hợp lỗi, giúp tối ưu hóa hiệu suất và đảm bảo độ tin cậy của pipeline.

---

## 2.2. Xử lý dữ liệu phân tán

### 2.2.1. Khái niệm xử lý phân tán

Xử lý dữ liệu phân tán (Distributed Data Processing) là một phương pháp tiếp cận trong đó công việc xử lý dữ liệu được chia nhỏ và phân phối cho nhiều máy tính trong một cụm (cluster) để thực hiện đồng thời. Thay vì một máy tính đơn lẻ phải gánh chịu toàn bộ khối lượng công việc, hệ thống phân tán cho phép nhiều máy tính cùng làm việc song song, mỗi máy xử lý một phần dữ liệu, sau đó kết quả từ các máy được tổng hợp lại để tạo ra kết quả cuối cùng.

Ý tưởng cốt lõi của xử lý phân tán dựa trên nguyên lý "chia để trị" (divide and conquer). Một bài toán lớn được chia thành nhiều bài toán con nhỏ hơn, mỗi bài toán con được giao cho một node trong cluster xử lý độc lập. Cách tiếp cận này không chỉ giúp tăng tốc độ xử lý mà còn cho phép xử lý những tập dữ liệu có kích thước vượt quá khả năng của một máy đơn lẻ.

### 2.2.2. So sánh xử lý cục bộ vs phân tán

Để hiểu rõ hơn về lợi ích của xử lý phân tán, chúng ta cần so sánh với phương pháp xử lý cục bộ truyền thống. Trong xử lý cục bộ, tất cả dữ liệu và tính toán đều diễn ra trên một máy tính duy nhất. Phương pháp này đơn giản, dễ triển khai và phù hợp với các tập dữ liệu nhỏ. Tuy nhiên, khi kích thước dữ liệu tăng lên, xử lý cục bộ bộc lộ nhiều hạn chế nghiêm trọng.

Về mặt tốc độ, xử lý cục bộ bị giới hạn bởi số lượng CPU core và tốc độ xử lý của một máy. Khi dữ liệu lớn, thời gian xử lý tăng tuyến tính và có thể kéo dài hàng giờ hoặc thậm chí hàng ngày. Ngược lại, xử lý phân tán có thể tận dụng hàng chục, hàng trăm hoặc thậm chí hàng nghìn máy tính để xử lý song song, giảm đáng kể thời gian hoàn thành.

Về khả năng mở rộng, xử lý cục bộ bị giới hạn bởi phần cứng của máy. Khi cần xử lý nhiều dữ liệu hơn, giải pháp duy nhất là nâng cấp phần cứng (scale-up), điều này tốn kém và có giới hạn vật lý. Trong khi đó, xử lý phân tán cho phép mở rộng bằng cách thêm máy mới vào cluster (scale-out), một cách tiếp cận linh hoạt và tiết kiệm chi phí hơn.

Về khả năng chịu lỗi, xử lý cục bộ rất dễ bị ảnh hưởng bởi sự cố phần cứng. Nếu máy tính gặp lỗi, toàn bộ quá trình xử lý bị gián đoạn và dữ liệu có thể bị mất. Hệ thống phân tán được thiết kế với cơ chế sao lưu và phục hồi tự động, đảm bảo hệ thống vẫn hoạt động ngay cả khi một số node gặp sự cố.

### 2.2.3. Lợi ích của xử lý song song

Xử lý song song mang lại nhiều lợi ích quan trọng cho việc xử lý dữ liệu lớn. Lợi ích đầu tiên và rõ ràng nhất là tăng tốc độ xử lý. Theo lý thuyết, nếu một công việc có thể được chia đều cho N máy, thời gian xử lý sẽ giảm xuống còn 1/N so với xử lý trên một máy. Trong thực tế, do overhead của việc phân phối và tổng hợp dữ liệu, tốc độ tăng thường thấp hơn lý thuyết nhưng vẫn rất đáng kể.

Lợi ích thứ hai là khả năng xử lý dữ liệu có kích thước lớn hơn bộ nhớ RAM của một máy. Khi dữ liệu được phân tán trên nhiều máy, mỗi máy chỉ cần lưu trữ và xử lý một phần nhỏ của tổng dữ liệu. Điều này cho phép xử lý các tập dữ liệu có kích thước hàng terabytes hoặc petabytes mà không gặp vấn đề về bộ nhớ.

Lợi ích thứ ba là tận dụng hiệu quả tài nguyên phần cứng. Trong một cluster, tài nguyên CPU, RAM và ổ cứng của tất cả các máy được kết hợp lại, tạo thành một hệ thống có năng lực tính toán và lưu trữ vượt trội so với bất kỳ máy đơn lẻ nào.

Trong bối cảnh đồ án này, việc sử dụng vòng lặp Python thông thường để xử lý 120,000 ảnh là không hiệu quả. Khi dùng vòng lặp for để duyệt qua từng file ảnh, chương trình chỉ sử dụng một CPU core và xử lý tuần tự từng ảnh một. Với mỗi ảnh cần được load, resize, đưa qua model MobileNetV2 để trích xuất đặc trưng, thời gian xử lý cho toàn bộ dataset có thể lên đến nhiều giờ. Ngược lại, khi sử dụng Apache Spark, dữ liệu được tự động phân chia thành các partition và phân phối cho các Executor trên các Worker node. Mỗi Executor xử lý một partition độc lập và song song với các Executor khác, giúp giảm đáng kể thời gian xử lý và tận dụng được toàn bộ tài nguyên của cluster.

---

## 2.3. Hadoop HDFS

### 2.3.1. Giới thiệu HDFS

HDFS (Hadoop Distributed File System) là hệ thống file phân tán được thiết kế để lưu trữ các file có kích thước rất lớn trên một cụm máy tính. HDFS là thành phần lưu trữ chính của hệ sinh thái Hadoop, được phát triển dựa trên ý tưởng từ Google File System (GFS). HDFS được tối ưu hóa cho việc lưu trữ và truy xuất các file có kích thước từ gigabytes đến terabytes, phù hợp với các ứng dụng Big Data cần xử lý lượng dữ liệu khổng lồ.

Một trong những đặc điểm quan trọng nhất của HDFS là khả năng chịu lỗi cao (fault-tolerant). HDFS được thiết kế với giả định rằng các thành phần phần cứng có thể gặp sự cố bất cứ lúc nào, do đó hệ thống tự động sao lưu dữ liệu và có cơ chế phục hồi khi có lỗi xảy ra. HDFS cũng được tối ưu cho việc đọc tuần tự (sequential read) với mô hình write-once, read-many, nghĩa là dữ liệu được ghi một lần và đọc nhiều lần, phù hợp với các ứng dụng phân tích dữ liệu.

### 2.3.2. Kiến trúc HDFS (NameNode, DataNode)

HDFS sử dụng kiến trúc Master-Slave với hai thành phần chính là NameNode và DataNode. NameNode đóng vai trò là Master, chịu trách nhiệm quản lý metadata của hệ thống file, bao gồm thông tin về cấu trúc thư mục, tên file, quyền truy cập và quan trọng nhất là vị trí của các block dữ liệu trên các DataNode. NameNode không lưu trữ dữ liệu thực tế mà chỉ lưu trữ thông tin về dữ liệu, giống như một cuốn sổ mục lục của thư viện.

DataNode đóng vai trò là Slave, chịu trách nhiệm lưu trữ dữ liệu thực tế. Mỗi DataNode lưu trữ các block dữ liệu và định kỳ gửi báo cáo về trạng thái của mình cho NameNode. Khi client muốn đọc hoặc ghi dữ liệu, nó sẽ liên hệ với NameNode để lấy thông tin về vị trí các block, sau đó trực tiếp giao tiếp với các DataNode để thực hiện thao tác đọc/ghi. Kiến trúc này giúp giảm tải cho NameNode và tăng hiệu suất của hệ thống.

Trong đồ án này, cluster được triển khai với một NameNode (truy cập qua port 9870) và một DataNode. Mặc dù đây là cấu hình tối thiểu, nó vẫn đủ để minh họa các khái niệm cơ bản của HDFS và đáp ứng yêu cầu của đồ án.

### 2.3.3. Cơ chế hoạt động (Block, Replication)

HDFS chia mỗi file thành các block có kích thước cố định, mặc định là 128MB (có thể cấu hình). Việc chia file thành các block nhỏ hơn giúp HDFS có thể lưu trữ các file có kích thước lớn hơn dung lượng của một ổ đĩa đơn lẻ, đồng thời cho phép xử lý song song các phần khác nhau của file. Ví dụ, một file 512MB sẽ được chia thành 4 block, mỗi block 128MB, và các block này có thể được lưu trữ trên các DataNode khác nhau.

Để đảm bảo độ tin cậy của dữ liệu, HDFS sử dụng cơ chế replication (sao chép). Mỗi block được sao chép ra nhiều bản (mặc định là 3 bản) và các bản sao được lưu trữ trên các DataNode khác nhau. Khi một DataNode gặp sự cố, dữ liệu vẫn có thể được truy xuất từ các bản sao trên các DataNode khác. NameNode liên tục theo dõi số lượng bản sao của mỗi block và tự động tạo thêm bản sao nếu số lượng giảm xuống dưới ngưỡng cấu hình.

Theo yêu cầu của đồ án, dữ liệu đầu vào thô (Raw Data) phải được upload lên HDFS trước khi xử lý, không được đọc trực tiếp từ ổ cứng máy thật (Local OS). Trong đồ án này, 120,000 ảnh từ dataset CIFAKE được upload lên HDFS tại đường dẫn /data/cifake/, Spark đọc dữ liệu từ HDFS để xử lý, và kết quả được ghi ngược lại HDFS tại các đường dẫn /processed/, /results/ và /models/.

---

## 2.4. Apache Spark

### 2.4.1. Giới thiệu Apache Spark

Apache Spark là một framework xử lý dữ liệu phân tán mã nguồn mở, được phát triển ban đầu tại UC Berkeley vào năm 2009 và sau đó trở thành dự án Apache vào năm 2013. Spark được thiết kế để xử lý dữ liệu lớn với tốc độ cao, nổi bật với khả năng xử lý in-memory (trong bộ nhớ), giúp nhanh hơn Hadoop MapReduce từ 10 đến 100 lần trong nhiều trường hợp.

Spark hỗ trợ nhiều ngôn ngữ lập trình bao gồm Python (PySpark), Scala, Java và R, giúp các nhà phát triển có thể sử dụng ngôn ngữ quen thuộc của mình. Spark cũng cung cấp một hệ sinh thái phong phú với các thư viện tích hợp như Spark SQL cho xử lý dữ liệu có cấu trúc, Spark Streaming cho xử lý dữ liệu thời gian thực, MLlib cho machine learning, và GraphX cho xử lý đồ thị. Trong đồ án này, chúng ta sử dụng PySpark kết hợp với Spark MLlib để xây dựng pipeline phát hiện ảnh Deepfake.

### 2.4.2. Kiến trúc Spark (Driver, Executor, Worker)

Kiến trúc của Spark bao gồm bốn thành phần chính: Driver, Cluster Manager, Worker Node và Executor. Driver là chương trình chính chứa hàm main() của ứng dụng Spark, chịu trách nhiệm tạo SparkContext, định nghĩa các transformation và action trên dữ liệu, và điều phối toàn bộ quá trình thực thi job. Driver phân tích code của người dùng, tạo ra DAG (Directed Acyclic Graph) của các stage và task, sau đó gửi các task này đến các Executor để thực thi.

Cluster Manager là thành phần quản lý tài nguyên của cluster, chịu trách nhiệm phân bổ tài nguyên (CPU, memory) cho các ứng dụng Spark. Spark hỗ trợ nhiều loại Cluster Manager khác nhau bao gồm Standalone (built-in), Apache YARN, Apache Mesos và Kubernetes. Trong đồ án này, chúng ta sử dụng Standalone Cluster Manager với Spark Master lắng nghe trên port 7077.

Worker Node là các máy vật lý hoặc ảo trong cluster, nơi các Executor được khởi chạy. Mỗi Worker Node có thể chạy một hoặc nhiều Executor tùy thuộc vào cấu hình tài nguyên. Executor là process JVM chạy trên Worker Node, chịu trách nhiệm thực thi các task được giao bởi Driver và lưu trữ dữ liệu trong bộ nhớ hoặc ổ đĩa. Mỗi Executor có một lượng memory và số CPU core được cấp phát cố định.

### 2.4.3. RDD và DataFrame

RDD (Resilient Distributed Dataset) là cấu trúc dữ liệu cơ bản và nguyên thủy nhất của Spark. RDD là một tập hợp các phần tử được phân tán trên các node trong cluster, có khả năng chịu lỗi (resilient) nhờ cơ chế lineage (ghi nhớ chuỗi các transformation để có thể tái tạo dữ liệu khi cần). RDD là immutable, nghĩa là một khi được tạo ra thì không thể thay đổi, mọi transformation trên RDD sẽ tạo ra một RDD mới.

DataFrame là cấu trúc dữ liệu cấp cao hơn, được giới thiệu từ Spark 1.3, tổ chức dữ liệu theo dạng bảng với các cột có tên và kiểu dữ liệu xác định (schema). DataFrame được tối ưu hóa tốt hơn RDD nhờ Catalyst Optimizer, một query optimizer có khả năng tối ưu hóa các truy vấn trước khi thực thi. API của DataFrame dễ sử dụng hơn, giống với SQL và pandas, giúp các nhà phân tích dữ liệu có thể làm việc hiệu quả hơn. Trong đồ án này, DataFrame được sử dụng làm cấu trúc dữ liệu chính để lưu trữ và xử lý dữ liệu ảnh cũng như các vector đặc trưng.

### 2.4.4. Spark MLlib

Spark MLlib là thư viện Machine Learning của Spark, cung cấp các thuật toán và công cụ để xây dựng các ứng dụng machine learning trên dữ liệu lớn. MLlib được thiết kế để chạy trên cluster, tận dụng khả năng xử lý phân tán của Spark để train model trên các tập dữ liệu có kích thước lớn mà các thư viện ML truyền thống không thể xử lý được.

MLlib cung cấp nhiều thuật toán phân loại (classification) bao gồm Logistic Regression, Decision Tree, Random Forest, Gradient Boosted Trees và Naive Bayes. Ngoài ra, MLlib còn hỗ trợ các thuật toán hồi quy (regression), phân cụm (clustering), và các công cụ feature extraction, transformation. MLlib cũng cung cấp Pipeline API, cho phép xây dựng các workflow machine learning phức tạp bằng cách kết hợp nhiều bước xử lý thành một pipeline thống nhất.

Theo yêu cầu của đồ án, không được sử dụng vòng lặp for của Python để duyệt qua từng file mà phải sử dụng Spark RDD hoặc DataFrame. Trong đồ án này, chúng ta sử dụng spark.read.parquet() để đọc dữ liệu, Spark UDF (User Defined Function) để trích xuất đặc trưng, và Spark MLlib RandomForestClassifier để train model phân loại.

---

## 2.5. Transfer Learning và MobileNetV2

### 2.5.1. Khái niệm Transfer Learning

Transfer Learning (Học chuyển giao) là một kỹ thuật trong machine learning, trong đó một model đã được huấn luyện trên một tập dữ liệu lớn (source domain) được sử dụng làm điểm khởi đầu cho một bài toán khác (target domain). Ý tưởng cốt lõi của Transfer Learning là kiến thức mà model học được từ một bài toán có thể được chuyển giao và áp dụng cho các bài toán liên quan, giúp tiết kiệm thời gian và tài nguyên tính toán đáng kể.

Transfer Learning đặc biệt hữu ích trong các trường hợp khi tập dữ liệu của bài toán mới có kích thước nhỏ, không đủ để train một model từ đầu. Thay vì train một mạng neural network với hàng triệu tham số từ random initialization, chúng ta có thể sử dụng các weights đã được học từ các tập dữ liệu lớn như ImageNet (với hơn 14 triệu ảnh và 1000 classes). Các features cấp thấp như edges, textures, shapes mà model học được từ ImageNet có thể được tái sử dụng cho nhiều bài toán computer vision khác nhau.

Có hai cách tiếp cận chính trong Transfer Learning. Cách thứ nhất là Feature Extraction, trong đó model pretrained được sử dụng như một feature extractor cố định, các weights không được cập nhật trong quá trình training, và chỉ có classifier mới được train trên các features đã trích xuất. Cách thứ hai là Fine-tuning, trong đó một phần hoặc toàn bộ model pretrained được train lại với learning rate nhỏ để điều chỉnh các weights cho phù hợp với bài toán mới. Trong đồ án này, chúng ta sử dụng cách tiếp cận Feature Extraction với MobileNetV2.

### 2.5.2. Kiến trúc MobileNetV2

MobileNetV2 là một kiến trúc Convolutional Neural Network (CNN) được Google phát triển và công bố vào năm 2018, được thiết kế đặc biệt cho các thiết bị di động và embedded systems với tài nguyên tính toán hạn chế. MobileNetV2 đạt được sự cân bằng tốt giữa độ chính xác và hiệu suất tính toán, với số lượng tham số chỉ khoảng 3.4 triệu, nhỏ hơn nhiều so với các kiến trúc như VGG16 (138 triệu) hay ResNet50 (25 triệu).

Đặc điểm nổi bật của MobileNetV2 là sử dụng Depthwise Separable Convolution, một kỹ thuật chia convolution thông thường thành hai bước: depthwise convolution (áp dụng một filter cho mỗi channel) và pointwise convolution (1x1 convolution để kết hợp các channels). Kỹ thuật này giảm đáng kể số phép tính so với convolution thông thường mà vẫn giữ được khả năng học các features phức tạp.

MobileNetV2 cũng giới thiệu kiến trúc Inverted Residuals với Linear Bottlenecks. Khác với residual block truyền thống (thu hẹp rồi mở rộng), inverted residual mở rộng channels trước bằng 1x1 convolution, sau đó áp dụng depthwise convolution, và cuối cùng thu hẹp lại bằng 1x1 convolution với linear activation. Cấu trúc này giúp giữ lại thông tin quan trọng trong quá trình xử lý.

Khi sử dụng MobileNetV2 cho feature extraction, ảnh đầu vào có kích thước 224x224x3 được đưa qua các lớp convolution của mạng, và output từ lớp global average pooling cuối cùng (trước lớp classification) là một vector 1280 chiều. Vector này chứa các đặc trưng cấp cao đã được học từ ImageNet và có thể được sử dụng làm input cho các classifier khác.

### 2.5.3. Feature Extraction (Vector 1280 chiều)

Trong đồ án này, MobileNetV2 được sử dụng để trích xuất đặc trưng từ các ảnh trong dataset CIFAKE. Quy trình trích xuất đặc trưng bao gồm các bước sau: đầu tiên, ảnh được đọc từ HDFS dưới dạng binary data; tiếp theo, ảnh được decode và resize từ kích thước gốc 32x32 lên 224x224 để phù hợp với input size của MobileNetV2; sau đó, pixel values được chuẩn hóa về khoảng phù hợp với model; cuối cùng, ảnh được đưa qua MobileNetV2 (không bao gồm lớp fully connected cuối) để lấy output là vector 1280 chiều.

Vector 1280 chiều này chứa các đặc trưng trừu tượng cấp cao của ảnh, bao gồm thông tin về textures, patterns, shapes và các đặc điểm khác mà model đã học được từ ImageNet. Mặc dù ImageNet không chứa các ảnh Deepfake, các features cấp thấp và trung bình mà MobileNetV2 học được vẫn có thể phân biệt được sự khác biệt giữa ảnh thật và ảnh được tạo bởi AI, vì ảnh Deepfake thường có các artifacts và patterns đặc trưng mà model có thể nhận ra.

Theo yêu cầu của đồ án, sinh viên không được sử dụng model Deepfake Detector có sẵn mà phải trích xuất đặc trưng từ các ảnh bằng model train trên ImageNet như ResNet50 hoặc MobileNetV2. Trong đồ án này, MobileNetV2 được chọn vì có kích thước nhỏ gọn, phù hợp với môi trường Docker container với tài nguyên hạn chế, đồng thời vẫn đạt được độ chính xác tốt.

---

## 2.6. Random Forest Classifier

### 2.6.1. Khái niệm Decision Tree

Decision Tree (Cây quyết định) là một thuật toán học máy có giám sát (supervised learning) sử dụng cấu trúc cây để đưa ra quyết định phân loại hoặc hồi quy. Cây quyết định mô phỏng quá trình ra quyết định của con người bằng cách chia bài toán thành các câu hỏi yes/no liên tiếp dựa trên các thuộc tính của dữ liệu.

Cấu trúc của Decision Tree bao gồm ba loại node: Root node là node gốc ở đỉnh cây, đại diện cho toàn bộ tập dữ liệu và là điểm bắt đầu của quá trình phân loại; Internal node là các node trung gian, mỗi node chứa một điều kiện kiểm tra trên một thuộc tính cụ thể; Leaf node là các node lá ở cuối cây, chứa kết quả phân loại cuối cùng. Quá trình phân loại một mẫu mới bắt đầu từ root node, đi theo các nhánh dựa trên kết quả của các điều kiện kiểm tra, cho đến khi đến leaf node để lấy kết quả.

Decision Tree có ưu điểm là dễ hiểu, dễ giải thích và có thể xử lý cả dữ liệu số và categorical. Tuy nhiên, Decision Tree đơn lẻ thường có xu hướng overfitting, đặc biệt khi cây quá sâu hoặc dữ liệu có nhiều nhiễu. Để khắc phục vấn đề này, các phương pháp ensemble như Random Forest được sử dụng.

### 2.6.2. Ensemble Learning - Random Forest

Random Forest là một thuật toán Ensemble Learning, kết hợp nhiều Decision Tree để đưa ra dự đoán chính xác và ổn định hơn so với một cây đơn lẻ. Ý tưởng cốt lõi của Random Forest là "wisdom of the crowd" - kết hợp ý kiến của nhiều "chuyên gia" (các cây quyết định) sẽ cho kết quả tốt hơn so với một chuyên gia đơn lẻ.

Random Forest sử dụng hai kỹ thuật chính để tạo ra sự đa dạng giữa các cây. Kỹ thuật thứ nhất là Bagging (Bootstrap Aggregating), trong đó mỗi cây được train trên một tập dữ liệu con được lấy mẫu ngẫu nhiên có hoàn lại (bootstrap sample) từ tập dữ liệu gốc. Điều này có nghĩa là mỗi cây được train trên một tập dữ liệu hơi khác nhau, giúp giảm variance và overfitting.

Kỹ thuật thứ hai là Random Feature Selection, trong đó tại mỗi node của cây, thay vì xem xét tất cả các features để tìm split tốt nhất, chỉ một tập con ngẫu nhiên các features được xem xét. Điều này tạo ra sự đa dạng giữa các cây và giảm correlation giữa chúng, giúp cải thiện hiệu suất của ensemble.

Khi dự đoán, mỗi cây trong forest đưa ra một vote cho class mà nó dự đoán, và kết quả cuối cùng là class nhận được nhiều vote nhất (majority voting). Trong bài toán phân loại ảnh Deepfake, mỗi cây sẽ vote cho REAL hoặc FAKE, và kết quả cuối cùng là class có đa số phiếu.

### 2.6.3. Các tham số quan trọng (numTrees, maxDepth)

Random Forest có nhiều hyperparameters có thể điều chỉnh để tối ưu hiệu suất. Tham số numTrees xác định số lượng cây trong forest, giá trị lớn hơn thường cho kết quả ổn định hơn nhưng tăng thời gian training và prediction. Trong đồ án này, numTrees được đặt là 100, một giá trị cân bằng giữa hiệu suất và thời gian tính toán.

Tham số maxDepth xác định độ sâu tối đa của mỗi cây, giới hạn số lượng splits từ root đến leaf. Giá trị maxDepth lớn cho phép cây học các patterns phức tạp hơn nhưng có nguy cơ overfitting, trong khi giá trị nhỏ có thể dẫn đến underfitting. Trong đồ án này, maxDepth được đặt là 15.

Tham số featureSubsetStrategy xác định số lượng features được xem xét tại mỗi split. Giá trị "sqrt" có nghĩa là căn bậc hai của tổng số features sẽ được xem xét, với 1280 features thì khoảng 36 features được xem xét tại mỗi node. Đây là giá trị mặc định và thường hoạt động tốt cho các bài toán classification.

Trong đồ án này, Random Forest nhận input là vector 1280 chiều từ MobileNetV2 và output là nhãn 0 (REAL) hoặc 1 (FAKE). Với 100 cây quyết định, mỗi cây sẽ vote cho một class, và kết quả cuối cùng được quyết định bởi đa số phiếu.

---

## 2.7. Các chỉ số đánh giá mô hình

### 2.7.1. Confusion Matrix (TP, TN, FP, FN)

Confusion Matrix (Ma trận nhầm lẫn) là một công cụ quan trọng để đánh giá hiệu suất của các mô hình phân loại. Ma trận này tổng hợp kết quả dự đoán của model so với nhãn thực tế, cho phép chúng ta hiểu rõ hơn về các loại lỗi mà model mắc phải. Trong bài toán phân loại nhị phân như phát hiện ảnh Deepfake, Confusion Matrix có kích thước 2x2 với bốn thành phần chính.

True Positive (TP) là số lượng mẫu được dự đoán đúng là positive (FAKE). Trong bối cảnh đồ án, đây là số ảnh FAKE được model nhận diện chính xác là FAKE. True Negative (TN) là số lượng mẫu được dự đoán đúng là negative (REAL), tức là số ảnh REAL được model nhận diện chính xác là REAL.

False Positive (FP) là số lượng mẫu bị dự đoán sai là positive trong khi thực tế là negative. Trong bối cảnh đồ án, đây là số ảnh REAL bị model nhận nhầm là FAKE, còn được gọi là "false alarm" hay lỗi Type I. False Negative (FN) là số lượng mẫu bị dự đoán sai là negative trong khi thực tế là positive, tức là số ảnh FAKE bị model bỏ sót và nhận nhầm là REAL, còn được gọi là lỗi Type II.

Việc phân tích Confusion Matrix giúp chúng ta hiểu được model đang mắc loại lỗi nào nhiều hơn và từ đó có thể điều chỉnh ngưỡng quyết định hoặc cải thiện model cho phù hợp với yêu cầu của bài toán.

### 2.7.2. Accuracy, Precision, Recall, F1-Score

Từ Confusion Matrix, chúng ta có thể tính toán các chỉ số đánh giá quan trọng để đo lường hiệu suất của model một cách toàn diện.

Accuracy (Độ chính xác) là tỷ lệ dự đoán đúng trên tổng số mẫu, được tính bằng công thức (TP + TN) / (TP + TN + FP + FN). Accuracy cho biết tổng quan model dự đoán đúng bao nhiêu phần trăm. Trong đồ án này, Accuracy đạt 87.76%, có nghĩa là model đoán đúng khoảng 17,551 trong tổng số 20,000 ảnh test. Tuy nhiên, Accuracy có thể gây hiểu nhầm khi dữ liệu không cân bằng, vì vậy cần kết hợp với các chỉ số khác.

Precision (Độ chính xác dương) là tỷ lệ dự đoán đúng trong số các mẫu được dự đoán là positive, được tính bằng công thức TP / (TP + FP). Precision trả lời câu hỏi: "Trong số các ảnh mà model dự đoán là FAKE, bao nhiêu phần trăm thực sự là FAKE?". Precision cao có nghĩa là model ít mắc lỗi false positive, quan trọng trong các trường hợp khi chi phí của việc báo nhầm cao. Trong đồ án này, Precision đạt 87.78%.

Recall (Độ nhạy hay Sensitivity) là tỷ lệ dự đoán đúng trong số các mẫu thực sự là positive, được tính bằng công thức TP / (TP + FN). Recall trả lời câu hỏi: "Trong số các ảnh thực sự là FAKE, model phát hiện được bao nhiêu phần trăm?". Recall cao có nghĩa là model ít bỏ sót các mẫu positive, quan trọng trong các trường hợp khi chi phí của việc bỏ sót cao. Trong đồ án này, Recall đạt 87.76%.

F1-Score là trung bình điều hòa (harmonic mean) của Precision và Recall, được tính bằng công thức 2 × (Precision × Recall) / (Precision + Recall). F1-Score cung cấp một chỉ số cân bằng giữa Precision và Recall, hữu ích khi cần đánh giá tổng thể hiệu suất của model mà không thiên về một chỉ số nào. Trong đồ án này, F1-Score đạt 87.75%, cho thấy sự cân bằng tốt giữa khả năng phát hiện ảnh FAKE và tránh báo nhầm ảnh REAL.

Kết quả đánh giá cho thấy model MobileNetV2 kết hợp Random Forest đạt độ chính xác khoảng 88% trong việc phân loại ảnh REAL và FAKE. Các chỉ số Precision, Recall và F1-Score đều xấp xỉ nhau, cho thấy model hoạt động cân bằng và không thiên về một class nào. Kết quả này chứng minh rằng các đặc trưng trích xuất từ MobileNetV2 chứa đủ thông tin để phân biệt ảnh thật và ảnh Deepfake, và Random Forest có thể học được các patterns phân biệt từ các đặc trưng này.
