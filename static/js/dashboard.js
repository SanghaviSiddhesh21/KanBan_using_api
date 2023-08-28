const dashboard=Vue.component('dashboard',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info" class='dashboard-nav'>
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Create List</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Create Card</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>List Summary</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button> 
                            <b-nav-item href='#' @click="hide"><router-link to="/" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                    
                </div>
            </template>
        </b-sidebar>
    
        <div class = 'dashboard-main'>
            <template v-for='i in activelists'>
                <div class='dashboard-indiviual-list'>
                    <b-card-group deck>
                        <b-card header-tag="header" footer-tag="footer">
                            <template #header>
                                <h6 class="mb-0">{{i.listtitle}}</h6>
                            </template>
                            <div class='dashboard-list-card-container'>
                                <div v-for='j in i.activecards'>
                                    <b-card title="" sub-title="">
                                        <b-card-text>
                                            <h5>{{j.cardtitle}}</h5>
                                            <em>Due by: {{j.carddueby}}</em><br><br>
                                            {{j.carddescription}}
                                        </b-card-text>
                                        <button><router-link :to="{path:'/editcard',query: { cardid: j.cardid }}">Edit Card</router-link></button>
                                        <button><router-link :to="{path:'/deletecard',query: { cardid: j.cardid }}">Delete Card</router-link></button>
                                    </b-card>
                                </div>
                            </div>
                            <template #footer>
                            <form method="post" action='/ExportList' class='dashboard-list-export-form'>
                                    <button><router-link :to="{path:'/editlist',query: { listid: i.listid }}">Edit List</router-link></button>
                                    <button><router-link :to="{path:'/deletelist',query: { listid: i.listid }}">Delete List</router-link></button>
                                    <input type="text" v-model=i.listid name="listid" hidden>
                                    <button type="submit" class="btn btn-info btn-list-export">Export</button>
                                </form>
                            </template>
                        </b-card>
                    </b-card-group>
                </div>
            </template>         
        </div>
    </div>
    `,
    data:function(){
        return{
            activelists:[]
        }
    },
    mounted:function(){
        uid=document.getElementById('userid').value;
        // console.log(uid);
        // console.log('http://127.0.0.1:8080/api/createcardtablist/'+uid);
        url="http://127.0.0.1:8080/api/dashboarddata/"+uid;
        //console.log(url);
        fetch(url,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(res => res.json())
        .then(data => this.activelists=data)
    }

})

const createlist=Vue.component('createlist',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Create Card</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>List Summary</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                </div>
            </template>
        </b-sidebar>
        <div id='creatlist-main-body'>
            <h2>List Works!</h2>
            <label for='listname'>List Name:</label><br>
            <input v-model="listname" placeholder="Enter your list name" id='listname'><br><br>
            <label for='listdescription'>An overview about the purpose of the list</label><br>
            <textarea v-model="listdescription" id='listdescription' rows="4" cols="50"></textarea><br><br>
            <button v-on:click='createlist_createcard'>Create Card</button>
            <button v-on:click='createlist'>Add List</button>
        </div>
    </div>
    `,
    data:function(){
        return{
            listname:'',
            listdescription:'',
            userid:''
        }
    },
    methods:{
        createlist:function(){
            //console.log('hi');
            userid=document.getElementById('userid').value;
            //console.log('hi');
            listname=document.getElementById('listname').value;
            if(listname){
                listdescription=document.getElementById('listdescription').value;
                if(listdescription){
                    // console.log(userid);
                    // console.log(listname);
                    // console.log(listdescription);
                    data={
                        "user_id": userid,
                        "list_name": listname,
                        "list_description": listdescription
                    }
                    fetch("http://127.0.0.1:8080/api/createlist",{
                        method:'POST',
                        headers:{
                            'Content-Type':'application/json',
                        },
                        body:JSON.stringify(data),
                    }).then(
                        response=>response.json()
                    ).then(
                        data=>{
                            console.log(data);
                            router.push({ path: '/' })
                        }, 
                    ).catch((error) => {
                        console.log('Error:',error);
                    })
                }
                else{
                    alert('Enter a description for the list');
                }
            }
            else{
                alert('Enter a list name');
            }
        },
        createlist_createcard:function(){
            //console.log('hi');
            userid=document.getElementById('userid').value;
            //console.log('hi');
            listname=document.getElementById('listname').value;
            if(listname){
                listdescription=document.getElementById('listdescription').value;
                if(listdescription){
                    // console.log(userid);
                    // console.log(listname);
                    // console.log(listdescription);
                    data={
                        "user_id": userid,
                        "list_name": listname,
                        "list_description": listdescription
                    }
                    fetch("http://127.0.0.1:8080/api/createlist",{
                        method:'POST',
                        headers:{
                            'Content-Type':'application/json',
                        },
                        body:JSON.stringify(data),
                    }).then(
                        response=>response.json()
                    ).then(
                        data=>{
                            console.log(data);
                            router.push({ path: '/createcard' })
                        }
                    ).catch((error) => {
                        console.log('Error:',error);
                    })
                }
                else{
                    alert('Enter a description for the list');
                }
            }
            else{
                alert('Enter a list name');
            }
        }
    }
})

const createcard=Vue.component('createcard',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Create List</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>List Summary</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                </div>
            </template>
        </b-sidebar>
        <div id='createcard-main-body'>
            <h2>Card Works</h2>
            <label for='listselected'>Select a list</label><br>
            <select v-model="selected" id='selected' multiple="true">
            <template v-for='i in alllist'>
                <option v-bind:value=i.listid>{{i.listname}}</option>
            </template>
            </select><br><br>

            <label for='cardname'>Card Name:</label><br>
            <input name="cardname" id='cardname' placeholder="Enter your list name"><br><br>

            <label for='carddescription'>An overview about the purpose of the Card</label><br>
            <textarea id='carddescription' name="carddescription" rows="4" cols="50"></textarea><br><br>

            <label for='due'>Due by:</label><br>
            <input type='date' id='due' name='due'><br><br>

            <input type="checkbox" v-model="status" true-value="yes" false-value="no" />
            <label for="status">Mark as complete </label><br><br>

            <button v-on:click='createcard'>Create Card</button>
        </div>
    </div>
    `,
    data:function(){
        return{
            alllist:[],
            selected:[],
            status:'no'
        }
    },
    methods:{
        createcard: function(){
            //console.log(this.selected)
            user_id=document.getElementById('userid').value;
            console.log(user_id);
            if(this.selected){
                cardname=document.getElementById('cardname').value;
                if(cardname){
                    carddescription=document.getElementById('carddescription').value;
                    if(carddescription){
                        due=document.getElementById('due').value;
                        if(due){
                            //console.log(this.status);
                            data={
                                "user_id": user_id,
                                "card_name": cardname,
                                "card_description": carddescription,
                                "due":due,
                                "status":this.status,
                                "lists_to_add":JSON.stringify(this.selected)
                            }
                            console.log(data)
                            fetch("http://127.0.0.1:8080/api/createcard",{
                                method:'POST',
                                headers:{
                                    'Content-Type':'application/json',
                                },
                                body:JSON.stringify(data),
                            }).then(
                                response=>response.json()
                            ).then(
                                data=>{
                                    console.log(data);
                                    router.push({ path: '/' })
                                }
                            ).catch((error) => {
                                console.log('Error:',error);
                            })
                        }
                        else{
                            alert('Select a due date for the card to be created');
                        }
                    }
                    else{
                        alert('Write the description of the card to add');
                    }
                }   
                else{
                    alert('Write the name of the card to add');
                }
            }
            else{
                alert('Select a list to add a card in');
            }            
        }
    },
    mounted:function(){
        uid=document.getElementById('userid').value;
        // console.log(uid);
        // console.log('http://127.0.0.1:8080/api/createcardtablist/'+uid);
        url="http://127.0.0.1:8080/api/createcardtablist/"+uid;
        //console.log(url);
        fetch(url,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(res => res.json())
        .then(data => this.alllist=data)
    }
})

const listsummary=Vue.component('listsummary',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Create List</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Create Card</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                </div>
            </template>
        </b-sidebar>
        <template>
            <div class="accordion accordian-custom" role="tablist">
                <h2>Active List</h2>
                <template v-for='i in active'>
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block v-b-toggle.accordion variant="info">{{i.listname}}</b-button>
                            <form method="post" action='/ExportList'>
                                <span><strong>Total number of task assigned:</strong><em>{{i.totalcards}}</em></span>
                                <span><strong>Total number of task due: </strong><em>{{i.activecards}}</em></span>
                                <span><strong>Total number of task completed: </strong><em>{{i.completedcards}}</em></span>
                                <input type="text" v-model=i.Listid name="listid" hidden>
                                <button type='submit'>Export list</button>
                                <button><router-link :to="{path:'/deletelist',query: { listid: i.Listid }}">Delete List</router-link></button>
                            </form>
                        </b-card-header>

                        <b-collapse id="accordion" visible accordion="my-accordion" role="tabpanel">
                            <b-card-body>
                                <div>
                                    <b-table-simple hover small caption-top responsive>
                                    <b-thead head-variant="dark">
                                        <b-tr>
                                            <b-th>Card Name</b-th>
                                            <b-th>Card description</b-th>
                                            <b-th>Status</b-th>
                                            <b-th>Dueby</b-th>
                                            <b-th>Methods</b-th>
                                        </b-tr>
                                    </b-thead>
                                    <b-tbody v-for='j in i.Cards'>
                                        <b-tr>
                                            <b-td>{{j.cardtitle}}</b-td>
                                            <b-td>{{j.carddescription}}</b-td>
                                            <b-td>{{j.status}}</b-td>
                                            <b-td>{{j.due}}</b-td>
                                            <b-td>
                                                <button><router-link :to="{path:'/editcard',query: { cardid: j.cardid }}">Edit Card</router-link></button>
                                                <button><router-link :to="{path:'/deletecard',query: { cardid: j.cardid }}">Delete Card</router-link></button>
                                            </b-td>
                                        </b-tr>
                                    </b-tbody>
                                    </b-table-simple>
                                </div>
                            </b-card-body>
                        </b-collapse>
                    </b-card>
                </template>
            </div>
            <div class="accordion accordian-custom" role="tablist">
                <h2>Completed List</h2>
                <template v-for='i in completed'>
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block v-b-toggle.accordioncomplete variant="info">{{i.listname}}</b-button>
                            <form method="post" action='/ExportList'>
                            <span><strong>Total number of task assigned:</strong><em>{{i.totalcards}}</em></span>
                            <span><strong>Total number of task due: </strong><em>{{i.activecards}}</em></span>
                            <span><strong>Total number of task completed: </strong><em>{{i.completedcards}}</em></span>
                            <input type="text" v-model=i.Listid name="listid" hidden>
                            <button type='submit'>Export list</button>
                            <button><router-link :to="{path:'/deletelist',query: { listid: i.Listid }}">Delete List</router-link></button>
                            </form>
                        </b-card-header>

                        <b-collapse id="accordioncomplete" visible accordion="my-accordion" role="tabpanel">
                            <b-card-body>
                                <div>
                                    <b-table-simple hover small caption-top responsive>
                                    <b-thead head-variant="dark">
                                        <b-tr>
                                            <b-th>Card Name</b-th>
                                            <b-th>Card description</b-th>
                                            <b-th>Status</b-th>
                                            <b-th>Dueby</b-th>
                                            <b-th>Methods</b-th>
                                        </b-tr>
                                    </b-thead>
                                    <template v-for='j in i.Cards'>
                                        <b-tbody>
                                            <b-tr>
                                                <b-td>{{j.cardtitle}}</b-td>
                                                <b-td>{{j.carddescription}}</b-td>
                                                <b-td>{{j.status}}</b-td>
                                                <b-td>{{j.due}}</b-td>
                                                <b-td>
                                                    <button><router-link :to="{path:'/editcard',query: { cardid: j.cardid }}">Edit Card</router-link></button>
                                                    <button><router-link :to="{path:'/deletecard',query: { cardid: j.cardid }}">Delete Card</router-link></button>
                                                </b-td>
                                            </b-tr>
                                        </b-tbody>
                                    </template>
                                    </b-table-simple>
                                </div>
                            </b-card-body>
                        </b-collapse>
                    </b-card>
                </template>
            </div>
        </template>
    </div>
    `,
    data:function(){
        return{
            active:[],
            completed:[]
        }
    },
    mounted:function(){
        uid=document.getElementById('userid').value;
        console.log(uid);
        console.log('http://127.0.0.1:8080/api/getcompletedlist/'+uid);
        url1="http://127.0.0.1:8080/api/getcompletedlist/"+uid;
        console.log(url1);
        fetch(url1,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(res => res.json())
        .then(data => this.completed=data)
        url2="http://127.0.0.1:8080/api/getactivelist/"+uid;
        fetch(url2,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(res => res.json())
        .then(data => this.active=data)
        console.log(this.active)
        console.log(this.completed)
    }
})

const listreport=Vue.component('listreport',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Create List</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Create Card</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>List Summary</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button>
                            <b-nav-item href='#' @click="hide"><router-link to="/listreport" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                </div>
            </template>
        </b-sidebar>
        <div class = 'dashboard-main'>
            <template v-for="i in alllist">
                <div class='dashboard-indiviual-list'>
                    <b-card-group deck>
                        <b-card header-tag="header" footer-tag="footer">
                            <template #header>
                                <h6 class="mb-0">{{i.listname}}</h6>
                            </template>
                            <div class='dashboard-list-card-container'>
                                <span><em>Total cards created: </em><strong>{{i.totalcards}}</strong></span>
                                <span><em>Completed cards: </em><strong>{{i.completedcards}}</strong></span>
                                <span><em>Remaining cards: </em><strong>{{i.remainingcards}}</strong></span>
                                <template>
                                    <img v-bind:src=i.pie>
                                </template>
                            </div>
                            <template #footer>
                                
                            </template>
                        </b-card>
                    </b-card-group>
                </div>     
            </template>   
        </div>
    </div>
    `,
    data:function(){
        return{
            alllist:[],
        }
    },
    mounted:function(){
        uid=document.getElementById('userid').value;
        url="http://127.0.0.1:8080/api/userlistreport/"+uid;
        console.log(url);
        fetch(url,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(res => res.json())
        .then(data => this.alllist=data)
    }
})

const editcard=Vue.component('editcard',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Create List</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>List Summary</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                    
                </div>
            </template>
        </b-sidebar>
        <div id='createcard-main-body'>
            <h2>Card Works</h2>
            <label for='listselected'>Select a list</label><br>
            <select v-model="selected" id='selected' multiple="true">
            <template v-for='i in alllist'>
                <option v-bind:value=i.listid>{{i.listname}}</option>
            </template>
            </select><br><br>

            <label for='cardname'>Card Name:</label><br>
            <input name="cardname" id='cardname' placeholder="Enter your list name" v-model=listdata[0].cardtitle><br><br>

            <label for='carddescription'>An overview about the purpose of the Card</label><br>
            <textarea id='carddescription' name="carddescription" rows="4" cols="50" v-model=listdata[0].carddescription></textarea><br><br>

            <label for='due'>Due by:</label><br>
            <input type='date' id='due' name='due' v-model=listdata[0].carddue><br><br>

            <input type="checkbox" v-model="status" true-value="yes" false-value="no" />
            <label for="status">Mark as complete </label><br><br>

            <button v-on:click='createcard'>Create Card</button>
        </div>
    </div>
    `,
    data:function(){
        return{
            alllist:[],
            selected:[],
            status:'no',
            listdata:[],
            cardid:this.$route.query.cardid
        }
    },
    methods:{
        createcard: function(){
            //console.log(this.$route.query.cardid);
            //console.log(this.selected)
            user_id=document.getElementById('userid').value;
            //console.log(user_id);
            if(this.selected){
                cardname=document.getElementById('cardname').value;
                if(cardname){
                    carddescription=document.getElementById('carddescription').value;
                    if(carddescription){
                        due=document.getElementById('due').value;
                        if(due){
                            //console.log(this.status);
                            data={
                                "user_id": user_id,
                                "card_id": this.$route.query.cardid,
                                "card_name": cardname,
                                "card_description": carddescription,
                                "due":due,
                                "status":this.status,
                                "lists_to_add":JSON.stringify(this.selected)
                            }
                            console.log(data)
                            fetch("http://127.0.0.1:8080/api/posteditedcarddetails",{
                                method:'POST',
                                headers:{
                                    'Content-Type':'application/json',
                                },
                                body:JSON.stringify(data),
                            }).then(
                                response=>response.json()
                            ).then(
                                data=>{
                                    console.log(data);
                                    router.push({ path: '/' })
                                }
                            ).catch((error) => {
                                console.log('Error:',error);
                            })
                        }
                        else{
                            alert('Select a due date for the card to be created');
                        }
                    }
                    else{
                        alert('Write the description of the card to add');
                    }
                }   
                else{
                    alert('Write the name of the card to add');
                }
            }
            else{
                alert('Select a list to add a card in');
            }            
        }
    },
    mounted:function(){
        uid=document.getElementById('userid').value;
        // console.log(uid);
        // console.log('http://127.0.0.1:8080/api/createcardtablist/'+uid);
        url="http://127.0.0.1:8080/api/createcardtablist/"+uid;
        //console.log(url);
        fetch(url,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(res => res.json())
        .then(data => this.alllist=data)

        url1="http://127.0.0.1:8080/api/geteditcarddetails/"+this.$route.query.cardid;
        console.log(url1)
        fetch(url1,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(res => res.json())
        .then(data => this.listdata=data)
        console.log(this.listdata)
    }
})

const deletecard=Vue.component('deletecard',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info" class='dashboard-nav'>
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Create List</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Create Card</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>List Summary</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button>
                            <b-nav-item href='#' @click="hide"><router-link to="/" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                    
                </div>
            </template>
        </b-sidebar>
        <h1>Deletion Confirmation</h1>
        <button v-on:click='deletecard'>Delete Card</button>
    </div>
    `,
    methods:{
        deletecard:function(){
            console.log(this.$route.query.cardid)
            data={
                "card_id": this.$route.query.cardid,
            }
            console.log(data)
            fetch("http://127.0.0.1:8080/api/deletecard",{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body:JSON.stringify(data),
            }).then(
                response=>response.json()
            ).then(
                data=>{
                    console.log(data);
                    router.push({ path: '/listsummary' })
                }
            ).catch((error) => {
                console.log('Error:',error);
            })
        }
    }
})

const editlist=Vue.component('editlist',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Create Card</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>List Summary</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                </div>
            </template>
        </b-sidebar>
        <div id='creatlist-main-body'>
            <h2>List Works!</h2>
            <label for='listname'>List Name:</label><br>
            <input placeholder="Enter your list name" id='listname'  v-model=listdata[0].listtitle><br><br>
            <label for='listdescription'>An overview about the purpose of the list</label><br>
            <textarea id='listdescription' rows="4" cols="50" v-model=listdata[0].listdescription></textarea><br><br>
            <button v-on:click='editlist_createcard'>Create Card</button>
            <button v-on:click='editlist'>Add List</button>
        </div>
    </div>
    `,
    data:function(){
        return{
            listname:'',
            listdescription:'',
            userid:'',
            listdata:[],
            listid:this.$route.query.listid
        }
    },
    methods:{
        editlist:function(){
            //console.log('hi');
            userid=document.getElementById('userid').value;
            //console.log('hi');
            listname=document.getElementById('listname').value;
            if(listname){
                listdescription=document.getElementById('listdescription').value;
                if(listdescription){
                    // console.log(userid);
                    // console.log(listname);
                    // console.log(listdescription);
                    data={
                        "list_id":this.$route.query.listid,
                        "user_id": userid,
                        "list_name": listname,
                        "list_description": listdescription
                    }
                    fetch("http://127.0.0.1:8080/api/edittedlist",{
                        method:'POST',
                        headers:{
                            'Content-Type':'application/json',
                        },
                        body:JSON.stringify(data),
                    }).then(
                        response=>response.json()
                    ).then(
                        data=>{
                            console.log(data);
                            router.push({ path: '/' })
                        }, 
                    ).catch((error) => {
                        console.log('Error:',error);
                    })
                }
                else{
                    alert('Enter a description for the list');
                }
            }
            else{
                alert('Enter a list name');
            }
        },
        editlist_createcard:function(){
            //console.log('hi');
            userid=document.getElementById('userid').value;
            //console.log('hi');
            listname=document.getElementById('listname').value;
            if(listname){
                listdescription=document.getElementById('listdescription').value;
                if(listdescription){
                    // console.log(userid);
                    // console.log(listname);
                    // console.log(listdescription);
                    data={
                        "list_id":this.$route.query.listid,
                        "user_id": userid,
                        "list_name": listname,
                        "list_description": listdescription
                    }
                    fetch("http://127.0.0.1:8080/api/edittedlist",{
                        method:'POST',
                        headers:{
                            'Content-Type':'application/json',
                        },
                        body:JSON.stringify(data),
                    }).then(
                        response=>response.json()
                    ).then(
                        data=>{
                            console.log(data);
                            router.push({ path: '/createcard' })
                        }
                    ).catch((error) => {
                        console.log('Error:',error);
                    })
                }
                else{
                    alert('Enter a description for the list');
                }
            }
            else{
                alert('Enter a list name');
            }
        }
    },
    mounted:function(){
        url1="http://127.0.0.1:8080/api/editlistdata/"+this.$route.query.listid;
        console.log(url1)
        fetch(url1,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
            },
        })
        .then(res => res.json())
        .then(data => this.listdata=data)
        //console.log(this.listdata)
    }
})

const deletelist=Vue.component('deletelist',{
    template:`
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info" class='dashboard-nav'>
            <b-navbar-brand href="#">
                <router-link to="/" id='navbar-title'>Lista</router-link>
            </b-navbar-brand>
            <template>
                <div>
                    <b-button v-b-toggle.sidebar-no-header id='sidebar-toggle-icon'><i class="bi bi-three-dots-vertical"></i></b-button>
                </div>
            </template>
        </b-navbar>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
            <template #default="{ hide }">
                <div class="p-3" id='sidebar-body'>
                    <h4 id="sidebar-no-header-title">Explore</h4>
                    <nav class="mb-3">
                        <b-nav horizontal>
                            <b-nav-item href='#' @click="hide"><router-link to="/createlist" class='sidebar-options'>Create List</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/createcard" class='sidebar-options'>Create Card</router-link></b-nav-item>
                            <b-nav-item href='#' @click="hide"><router-link to="/listsummary" class='sidebar-options'>List Summary</router-link></b-nav-item>
                            <button type='submit'><a href='/ListReport'>List Report</a></button>
                            <button type='submit'><a href='/Logout'>Logout</a></button>
                            <b-nav-item href='#' @click="hide"><router-link to="/" class='sidebar-options'>Close</router-link></b-nav-item>
                        </b-nav>
                    </nav>
                    
                </div>
            </template>
        </b-sidebar>
        <h1>Deletion Confirmation</h1>
        <button v-on:click='deletelist'>Delete List</button>
    </div>
    `,
    methods:{
        deletelist:function(){
            console.log(this.$route.query.cardid)
            data={
                "list_id": this.$route.query.listid,
            }
            console.log(data)
            fetch("http://127.0.0.1:8080/api/deletelist",{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body:JSON.stringify(data),
            }).then(
                response=>response.json()
            ).then(
                data=>{
                    console.log(data);
                    router.push({ path: '/' })
                }
            ).catch((error) => {
                console.log('Error:',error);
            })
        }
    },
    mounted:function(){
        console.log(this.$route.query.cardid)
    }
})

const routes=[{
    path:'/',
    component:dashboard
},{
    path:'/createlist',
    component:createlist
},{
    path:'/createcard',
    component:createcard
},{
    path:'/listsummary',
    component:listsummary
},{
    path:'/listreport',
    component:listreport
},{
    path:'/editcard',
    component:editcard,
    props(route) {
        return {  cardid: route.query.cardid }
    }
},{
    path:'/deletecard',
    component:deletecard,
    props(route) {
        return {  cardid: route.query.cardid }
    }
},{
    path:'/editlist',
    component:editlist,
    props(route) {
        return {  listid: route.query.listid }
    }
},{
    path:'/deletelist',
    component:deletelist,
    props(route) {
        return {  listid: route.query.listid }
    }
}
]

const router=new VueRouter({
    routes
})

var app= new Vue({
    el:"#app",//takes the id 
    router:router
})