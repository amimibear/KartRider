//by 啊咪咪小熊
#include <iostream>
#include <fstream>
using namespace std;
#define N 26//小屋边长

int o=0,a[N+2][N+2],s,f[9][600],g[9],m=140000;
int xh[100],yh[100],dh[100];
int check(int h);
void init();

int FJ = 10; //林中飞机个数
int JT = 0; //神翼祭坛个数
int TL = 0; //精灵塔楼个数
int ZX = 0; //臻享环绕个数
int XX = 2; //小新雕像个数
int PZB = 6; //拍照板个数
int MG = 1; //有无魔怪
int CB = 1; //有无怪诞城堡
int YL = 1; //有无永恒之月
int MT = 1; //有无魔毯

int HYB = 100; //sonic合影板个数（默认足够）
int LP = 100; //我的小屋路牌个数（默认足够）
int XK = 1; //有无新秀相框（不影响布局）
int DZ = 1; //有无音阶地砖（不影响布局）

int main()
{
    for(int i=1;i<600;i++) f[1][i]=115; for(int i=1;i<=2*PZB+1;i++) f[1][i]=120+i%2*20; for(int i=1;i<=LP;i++) f[1][2*PZB+1+i]=120; f[1][2*PZB+4]=360-f[1][2*PZB+2]-f[1][2*PZB+3];
    f[1][2*PZB+5]=140; for(int i=1;i<=LP;i++) f[1][2*PZB+5+i]=120; //若超过2个独立1*1且拍照板没用完，需要削减 若>=4个独立1*1且无4连，需要至少-20，小屋路牌不够减更多
    int i=1; if(MG) f[2][i++]=619; for(int j=0;j<XX;j++) f[2][i++]=580; f[2][i]=520; if(YL) {for(int j=i+2;j>2;j--) f[2][j]=f[2][j-2]; f[2][2]=1200-f[2][1];}//若超过一个2*2且无永恒之月，需要削减1
    for(int i=1;i<600;i++) f[3][i]=1080; for(int i=1;i<=HYB;i++) f[3][i]=1400; f[3][HYB+1]=f[3][HYB+2]=1380; f[3][HYB+3]=1180; //1080 不超过5个
    for(int i=1;i<600;i++) f[4][i]=2420; f[4][1]=2640;f[4][1+MT]=2640; for(int i=1;i<=TL;i++)f[4][1+MT+i]=2500;for(int i=1;i<=TL;i++)f[4][1+MT+TL+i]=2460;
    for(int i=1;i<600;i++) f[5][i]=4200; f[5][1]=4560;f[5][2]=4240;
    for(int i=1;i<600;i++) f[6][i]=5780; for(int i=1;i<=1+FJ;i++) f[6][i]=6320; for(int i=1;i<=JT;i++) f[6][1+FJ+i]=6200; f[6][FJ+JT+2]=f[6][FJ+JT+3]=5840; //1表示旋转木马 精灵巨树无限
    for(int i=1;i<600;i++) f[7][i]=0; f[7][1]=9180;
    for(int i=1;i<600;i++) f[8][i]=0; f[8][1]=f[8][2]=11800;
    
    for(int i=1;i<=8;i++) f[i][0]=0;
    for(int i=1;i<=8;i++) for(int j=1;j<600;j++) f[i][j]+=f[i][j-1];//改为累加和
    
    int n[9];
    for(int o6=0;o6<=1;o6++)
    for(n[8]=2;n[8]>=0;n[8]--)
    for(n[7]=CB;n[7]>=0;n[7]--)
    for(n[6]=o6?(N*N-80-64*n[8]-49*n[7])/36:min(1+FJ+JT,N*N-80-64*n[8]-49*n[7]);n[6]>=(o6?min(1+FJ+JT,N*N-80-64*n[8]-49*n[7])+1:0);n[6]--)//先从1+FJ+JT搜，再从最大搜
    for(n[5]=(N*N-80-64*n[8]-49*n[7]-36*n[6])/25;n[5]>=0;n[5]--)
    for(n[4]=(N*N-80-64*n[8]-49*n[7]-36*n[6]-25*n[5])/16;n[4]>=0;n[4]--)
    for(n[3]=(N*N-80-64*n[8]-49*n[7]-36*n[6]-25*n[5]-16*n[4])/9;n[3]>=0;n[3]--)
    {
        int o=1,oo=1;
        for(n[2]=min(MG+2*YL+XX+1,(N*N-80-64*n[8]-49*n[7]-36*n[6]-25*n[5]-16*n[4]-9*n[3])/4);n[2]>=0;n[2]--)
        {
            n[1]=N*N-80-64*n[8]-49*n[7]-36*n[6]-25*n[5]-16*n[4]-9*n[3]-4*n[2];
            int ff=9400+4360+4394+20230-148*(1-XK)-338*(1-DZ);//小屋+背景+地砖+室内
            for(int i=1;i<=8;i++) ff+=f[i][n[i]];
            if(ff>=m&&oo)// >
            {
                cout<<ff<<' ';
                for(int i=8;i>=1;i--) cout<<i<<':'<<n[i]<<' ';
                cout<<endl;
                
                if(o) //如果2*2全都打散成1*1都不行，那就肯定不行
                {
                    o=0;
                    g[1]=N*N-80-64*n[8]-49*n[7]-36*n[6]-25*n[5]-16*n[4]-9*n[3];
                    g[2]=0;
                    g[3]=n[3];g[4]=n[4];g[5]=n[5];g[6]=n[6];g[7]=n[7];g[8]=n[8];
                    init();
                    oo=check(0);
                }
                
                for(int i=1;i<=8;i++) g[i]=n[i];
                init();
                if(check(0))
                {
                    m=ff;
                    cout<<endl<<ff<<"! ";
                    for(int i=8;i>=1;i--) cout<<i<<':'<<n[i]<<' '; cout<<endl;
                    int num=0;
                    for(int i=1;i<=8;i++) num+=n[i];
                    for(int i=0;i<num;i++) cout<<dh[i]<<' '<<xh[i]<<' '<<yh[i]<<endl;
                    cout<<endl;
                    
                    ofstream fout;
                    fout.open("out.txt",ios::out);
                    fout<<num<<endl;
                    for(int i=0;i<num;i++) fout<<dh[i]<<' '<<xh[i]<<' '<<yh[i]<<endl;
                    fout.close();
                }
            }
        }
    }
}

int check(int h)
{
    //if(h<=12) cout<<h<<endl;
    int x=0,y=0,dx=1,dy=1;
    for(int j=1;j<=N;j++) //从左到右 从上到下找到第一个空格
    {
        for(int i=1;i<=N;i++) if(!a[i][j]) {x=i;y=j;break;}
        if(x) break;
    }
    while(!a[x+dx][y]&&dx<8) dx++; //x方向能延伸几格
    while(!a[x][y+dy]&&dy<8) dy++; //y方向能延伸几格
    int md=min(dx,dy);
    if(x<10&&y<5) md=min(md,max(10-x,5-y)); //考虑出生点阻挡
    
    xh[h]=x;yh[h]=y;
    
    for(int d=md;d>=1;d--) if(g[d])
    {
        dh[h]=d;
        for(int i=x;i<x+d;i++) for(int j=y;j<y+d;j++) a[i][j]=1;
        s-=d*d;
        g[d]--;
        if(!s) return 1;
        if(check(h+1)) return 1;
        g[d]++;
        s+=d*d;
        for(int i=x;i<x+d;i++) for(int j=y;j<y+d;j++) a[i][j]=0;
    }
    return 0;
}

void init()
{
    s=N*N-80;
    for(int i=0;i<=N+1;i++) for(int j=0;j<=N+1;j++) a[i][j]=0;
    for(int i=0;i<=N+1;i++) a[i][0]=a[i][N+1]=a[0][i]=a[N+1][i]=1;//边框
    for(int i=1;i<=6;i++) for(int j=1;j<=8;j++) a[i][j]=1;//小屋
    for(int i=1;i<=14;i++) for(int j=N-1;j<=N;j++) a[i][j]=1;//停车场
    for(int i=10;i<=11;i++) for(int j=5;j<=6;j++) a[i][j]=1;//出生点
}
