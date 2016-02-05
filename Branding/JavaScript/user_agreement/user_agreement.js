define(function(){
  return {
    user_db_url:'/api/v1/users/'+ ENV.current_user_id +'/custom_data/user_agreement',
    agreement_url:null,
    ns: window.location.hostname,
    showAgreement: function(){
      var _this = this;
      $('body').append('<div id="ext_aup_agreement"></div>');
      $("#ext_aup_agreement").load(this.agreement_url).dialog({
        modal:true,
        height:600,
        width:600,
        buttons: [ 
          { text: "I agree", click: function() {  _this.signAgreement($( this )); } } 
        ],
        create:function () {
            $(this).closest(".ui-dialog")
                .find(".ui-button:first") // the first button
                .addClass("btn-primary");
        }
      }); 
    },
    signAgreement: function(_d1){
      $.cookie(this.ns+'-ck',true);
      var params = {
        data : {
          ns:this.ns,
          data:true
        },
        type:'PUT',
        cache:false
      };
      // Send API request to Canvas API, store this signing
      // TODO put in a spinner
      $.ajax(this.user_db_url,params).done(function(_d){
        _d1.dialog( 'close' );
      });
      /*
      */

    },
    configure: function(config){
        this.aggreement_url = config.agreement_url;
        if(config.namespace!==null){
            this.ns = config.namespace;
        }
        console.log('configured');
        console.log('au',this.aggreement_url);
        console.log('ns',this.ns);
        return this;
    },
    check:function(agreement_url){
      if(agreement_url!==undefined){
        this.agreement_url = agreement_url;
      }
      this.checkAlreadyAgreed(this.afterCheck);
    },
    afterCheck:function(agree_or_not,_this){
      if(agree_or_not==false){
        _this.showAgreement();
      }
    },
    checkAlreadyAgreed: function(callback){
      // check here for the cookie
      var true_or_false = $.cookie(this.ns+'-ck');
      if(true_or_false===null){ true_or_false = false; }
      if(!true_or_false){
        var params = {ns:this.ns};
        _this = this;
        $.get(this.user_db_url,params).done(function(_d){
          callback(true,_this);
        }).error(function(_d){
          callback(false,_this);
        });
      }else{
        callback(true_or_false);
      }
    }
  }
});
