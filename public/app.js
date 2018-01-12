    new Vue({
      el: '#app',
      data: function() {
        return {
            captchaSrc: '/captcha?t=' + new Date().valueOf(),
            lNumber: null,
            operator: '',
            rNumber: null,
            options: ['','+','-','*','/']
        }
      },
      methods:{
          updateCaptcha: function(){
              console.log('@@@@ data: ' + this.lNumber + ' ' + this.operator + ' ' + this.rNumber);
              if(!this.lNumber || !this.operator || !this.rNumber){
                  var message = '请输入';
                  if(!this.lNumber){
                      message += '第一个数字';
                  }else if(!this.operator){
                      message += '运算符';
                  }else if(!this.rNumber){
                      message += '第二个数字';
                  }
                  const h = this.$createElement;
                  this.$notify({
                      title: '输入错误',
                      message: h('i', { style: 'color: teal'}, message)
                  });
                  return;
              }

              var that = this;

            fetch('/submit', {
                method: 'POST',
                body: JSON.stringify({
                    lNumber: this.lNumber,
                    operator: this.operator,
                    rNumber: this.rNumber
                }),
                headers: {
						'content-type': 'application/json'
					}
            })
                .then(function(){
                    that.captchaSrc = '/captcha?t=' + new Date().valueOf();
                    that.lNumber = null;
                    that.rNumber = null;
                    that.operator = '';
                })

          }
      }

    });