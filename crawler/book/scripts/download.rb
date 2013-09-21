#-*-coding:utf-8

require "open-uri"
require 'mongo'
include Mongo

#http://www.hao123.se/files/article/image/0/457/457s.jpg
# url是否是那个规律
def download(bid)
  page = 0
  if bid.length > 3 then
    page = bid[0, bid.length-3]
  end
    uri = "http://www.hao123.se/files/article/image/#{page}/#{bid}/#{bid}s.jpg"
    open(uri) {|f|
      File.open("../pics/#{bid}.jpg","wb") do |file|
        file.puts f.read
      end
    }
end

def hao123_main
  mongo_client = MongoClient.new("localhost", 27017)
  db = mongo_client.db("xiaoshuo_pict")
  coll = db["Book"]
  coll.find.each do |row|
    print "正在下载:", row["title"], "的图片\n"
    begin
      download row['bid']
    rescue
      puts "下载错误"
      next
    end
  end
end

def qidian_main(fname="nonpict_book.txt")
  File.open fname do |file|
    url = "http://image.cmfu.com/books/%s/%s.jpg"
    file.each_line do |line|
      if line[0] != "#" then 
        attrs = line.split("\t")
        qidian_id = attrs[2].chomp
        tempurl = url % [qidian_id, qidian_id]
        print "正在下载:", attrs[1], "的图片\n"
        open(tempurl) do |f|
          File.open("../pics/full/#{attrs[0]}.jpg","wb") do |file|
            file.puts f.read
          end
        end
      end
    end
  end
end
#hao123_main
qidian_main
