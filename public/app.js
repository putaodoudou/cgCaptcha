    new Vue({
      el: '#app',
      data: function() {
        return {
            captchaSrc: 'http://zhengzu.cangoonline.net/cas/imageAuthentication?timeTmp=' + new Date().valueOf(),
            lNumber: null,
            operator: '',
            rNumber: null,
            options: ['','+','-','*','/']
        }
      },
      methods:{
          updateCaptcha: function(){
              console.log('@@@@ data: ' + this.lNumber + ' ' + this.operator + ' ' + this.rNumber);
            this.captchaSrc = 'http://zhengzu.cangoonline.net/cas/imageAuthentication?timeTmp=' + new Date().valueOf();
            this.lNumber = null;
            this.rNumber = null;
            this.operator = '';
          }
      }

    });