export const BaiduStatistics = () => {
    return (
        <>
            <script dangerouslySetInnerHTML={getAnalyticsTag()} />
        </>
    )
};
 
const getAnalyticsTag = () => {
    return {
        __html: `
      var _hmt = _hmt || [];
      (function() {
        var hm = document.createElement("script");
        hm.src = "https://hm.baidu.com/hm.js?c77e5a3ef513ef219e1e4cbfa98a950e";
        var s = document.getElementsByTagName("script")[0];
        s.parentNode.insertBefore(hm, s);
      })();`,
    }
}