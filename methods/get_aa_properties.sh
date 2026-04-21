curl https://www.genome.jp/ftp/db/community/aaindex/aaindex1 |
awk '
    BEGIN{
        FS=" "
        print "Description,A,R,N,D,C,Q,E,G,H,I,L,K,M,F,P,S,T,W,Y,V"
        x=0
    }
    x==2 {
        k=$0
        gsub(/ +/, ",", k)
        print y k
        x=0
    }
    x==1 {
        k=$0
        gsub(/ +/, ",", k)
        y=y k
        x=2
    }
    $1=="D" {
        k=$0
        gsub(/"/, "´", k)
        y="\""substr(k, 3)"\""
    }
    $1=="I" {
        x=1
    }' - > ../results/properties.all.csv