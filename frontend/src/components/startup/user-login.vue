<template lang="html">
    <div>
        <div class="hint_text">管理员登录</div>
        <hr>
        <div class="error-msg" v-if="error_type == 504">登录失败，请检查登录密码！</div>
        <div class="error-msg" v-if="error_type == 502">用户名不存在！</div>
        <div class="error-msg" v-if="error_type == 500">未知错误！</div>
        <div class="error-msg" v-if="error_type == 503">非管理员用户！！</div>
        <div>
            <md-input-container md-inline>
                <md-icon><i class="ion-person"></i></md-icon>
                <label>用户名</label>
                <md-input v-model="username"></md-input>
            </md-input-container>
            <md-input-container md-inline>
                <md-icon><i class="ion-locked"></i></md-icon>
                <label>密码</label>
                <md-input v-model="password" type="password"></md-input>
            </md-input-container>
        </div>
        <div style="text-align: right;">
            <md-checkbox id="remember_me" name="rem" v-model="remember_me" style="float:left;">&nbsp;记住密码</md-checkbox>
            <md-button class="md-raised md-primary" :disabled="!enable_login" @click="login_submit">登录</md-button>
        </div>
    </div>
</template>

<script>
    import Vue from "vue";
    import Resource from 'vue-resource';
    Vue.use(Resource);

    let ajax = (method, url, data, on_success, on_fail) => {
        const ajax_info = {
            url: url,
            method: method,
            body: data
        };

        if(typeof(data) == "function"){
            on_fail    = on_success;
            on_success = data;
        }

        let vs = null;
        if(method == "GET"){
            vs = Vue.http.get(url);
        }else if(method == "POST"){
            vs = Vue.http.post(url, data);
        }
        vs.then((response)=>{
            try{
                let body = JSON.parse(response.body);
                if(body.status == "success"){
                    if(typeof(on_success) == "function"){
                        on_success(body["info"]);
                        return ;
                    }
                }else{
                    // not login
                    if(body.code == 403){
                        return ;
                    }
                    if(typeof(on_fail) == "function"){
                        on_fail(body["code"]);
                        return ;
                    }
                }
            }catch(e){
                if(typeof(on_fail) == "function"){
                    const error_code = 500;
                    on_fail(500);
                    return ;
                }
            }
        },(response)=>{
            if(typeof(on_fail) == "function"){
                on_fail(500);
                return ;
            }
        })
    }
    export default {
        data(){
            return {
                error_type : null,
                username : "",
                password : "",
                remember_me : false,
                enable_login : false
            }
        },
        computed:{
            enable_login(){
                if(this.password.length > 0 && this.username.length > 0){
                    return true;
                }else{
                    return false;
                }
            }
        },
        methods:{
            login_submit(){
                let _v = {
                    username : this.username,
                    password: this.password,
                    remember_me : this.remember_me
                };

                let vue = this;
                ajax("POST", "/super_admin/api/login", _v, (msg)=>{
                    window.location.href = "/super_admin/info"
                },(code)=>{
                    console.log(code);
                    vue.error_type = code;
                });
            }
        },
        mounted(){

        }
    };
</script>

<style>
.md-input-container{
    margin-bottom: 8px;
}

p{
    color : #666;
    margin-top: 12px;
    margin-bottom:6px;
}
</style>
