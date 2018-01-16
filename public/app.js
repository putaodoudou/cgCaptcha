    new Vue({
      el: '#app',
      data: function() {
        return {
            captchaSrc: '/captcha?t=' + new Date().valueOf(),
            lNumber: null,
            operator: '',
            rNumber: null,
            options: ['','+','-','*','/'],
            tiles: {

            }
        }
      },
      created:function(){
        var that = this;
        fetch('/query',{
            method: 'POST',
            headers: {
                    'content-type': 'application/json'
                }
            })
            .then(function(res){
                if(res && res.status === 200){
                    res.json()
                        .then(function(data){
                            that.tiles = data;
                        });
                }
            })
      },
      methods:{
          getImages: function(key){
              console.log('@@ key', key)
              return this.tiles[key];
          },
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
                .then(function(result){
                    if(result && result.status === 200){
                        result.json()
                            .then(function(data) {
                                for(var i =0; i < data.length; i++){
                                    var tuple = data[i];
                                    if(Object.keys(tuple).length === 1){
                                        var key = Object.keys(tuple)[0];
                                        var value = tuple[key];
                                        if(that.tiles.hasOwnProperty(key)){
                                            that.tiles[key].push(value);
                                        }else{
                                            that.tiles[key] = [];
                                            that.tiles[key].push(value);
                                        }
                                    }
                                }
                            });

                    }
                    that.captchaSrc = '/captcha?t=' + new Date().valueOf();
                    that.lNumber = null;
                    that.rNumber = null;
                    that.operator = '';
                    setTimeout(function(){
                        fetch('/predict', {method: 'POST', headers:{'content-type': 'application/json'}})
                            .then(function (result) {
                                if(result && result.status === 200){
                                    result.json()
                                        .then(function(data){
                                            console.log('@@@ predict', data)
                                        });
                                }
                            })

                    }, 500);
                })

          }
      }

    });