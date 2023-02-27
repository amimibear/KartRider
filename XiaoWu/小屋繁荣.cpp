//by 啊咪咪小熊
#include <iostream>
using namespace std;
#define N 26//小屋边长

int o=0,a[N+2][N+2],s,f[7][600],m=118175,g[7];
int xh[100],yh[100],dh[100];
int check(int h)
{
    //if(h<=12) cout<<h<<endl;
    int x=0,y=0,dx=1,dy=1;
    for(int j=1;j<=N;j++)
    {
        for(int i=1;i<=N;i++) if(!a[i][j]) {x=i;y=j;break;}
        if(x) break;
    }
    while(!a[x+dx][y]&&dx<6) dx++;
    while(!a[x][y+dy]&&dy<6) dy++;
    int md=min(dx,dy);
    if(x<10&&y<5) md=min(md,max(10-x,5-y));
    
    xh[h]=x;yh[h]=y;
    
    for(int d=md;d>=1;d--) if(g[d])
    {
        dh[h]=d;
        for(int i=x;i<x+d;i++) for(int j=y;j<y+d;j++) a[i][j]=1;
        s-=d*d;
        g[d]--;
        if(!s)
        {
            assert(!g[1]&&!g[2]&&!g[4]&&!g[5]&&!g[6]);
            //for(int i=1;i<=h;i++) cout<<i<<' '<<dh[i]<<' '<<xh[i]<<' '<<yh[i]<<endl;
            return 1;
        }
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
    for(int i=0;i<=N+1;i++) a[i][0]=a[i][N+1]=a[0][i]=a[N+1][i]=1;
    for(int i=1;i<=6;i++) for(int j=1;j<=8;j++) a[i][j]=1;//小屋
    for(int i=1;i<=14;i++) for(int j=N-1;j<=N;j++) a[i][j]=1;//停车场
    for(int i=10;i<=11;i++) for(int j=5;j<=6;j++) a[i][j]=1;//出生点
}

int main()
{
    for(int i=0;i<600;i++) f[1][i]=120+i%2*20;
    for(int i=0;i<600;i++) f[2][i]=520;
    f[2][1]=f[2][2]=580;f[2][3]=579;//先不考虑永恒之月
    //f[2][1]=f[2][2]=600;f[2][3]=f[2][4]=580;f[2][5]=579;再检查加上永恒之月的情况
    //如果不需要永恒之月肯定也不需要来玩鸭
    for(int i=0;i<600;i++) f[4][i]=2500;
    f[4][1]=2640;
    for(int i=0;i<600;i++) f[5][i]=4200;
    f[5][1]=4560;
    for(int i=0;i<600;i++) f[6][i]=6200;//5780;
    //f[6][1]=f[6][2]=5840;
    
    for(int i=1;i<=6;i++) f[i][0]=0;
    for(int i=1;i<=6;i++) for(int j=1;j<600;j++) f[i][j]+=f[i][j-1];//改为累加和

    int n[7]={0,0,0,0,0,0,0};
    //if(0)
    for(n[6]=(N*N-80)/36;n[6]>=1;n[6]--)
    for(n[5]=(N*N-80-36*n[6])/25;n[5]>=0;n[5]--)
    for(n[4]=(N*N-80-36*n[6]-25*n[5])/16;n[4]>=0;n[4]--)
    {
        int o=1,oo=1;
        for(n[2]=(N*N-80-36*n[6]-25*n[5]-16*n[4])/4;n[2]>=0;n[2]--)
        {
            n[1]=N*N-80-36*n[6]-25*n[5]-16*n[4]-4*n[2];
            int ff=9400+4360+6*N*N;//小屋+背景+地砖
            for(int i=1;i<=6;i++) ff+=f[i][n[i]];
            if(ff>=m&&oo)// >
            {
                cout<<ff<<' ';
                for(int i=1;i<=6;i++) cout<<n[i]<<' ';
                cout<<endl;
                
                if(o)
                {
                    o=0;
                    g[1]=N*N-80-36*n[6]-25*n[5]-16*n[4];
                    g[2]=0;
                    g[4]=n[4];g[5]=n[5];g[6]=n[6];
                    init();
                    oo=check(1);
                }
                
                for(int i=0;i<=6;i++) g[i]=n[i];
                init();
                if(check(1))
                {
                    m=ff;
                    cout<<endl<<ff<<'!';
                    for(int i=1;i<=6;i++) cout<<n[i]<<' ';
                    cout<<endl<<endl;
                    //return 0;
                }
            }
        }
    }
}

