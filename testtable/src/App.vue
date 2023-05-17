<template>
    <v-card class="p-64">
        <v-app>
            <template>
                <v-row justify="center">
                    <v-card-title class="text-h5">
                        Totally Random Movies
                    </v-card-title>
                </v-row>
                <v-row justify="absolute" class="ma-3">
                    <v-btn
                            color="green 1"
                            class="ma-2"
                            @click="adding = true"
                    >
                        Add new movie
                    </v-btn>
                    <v-card v-if="adding" class="mx-auto" max-width="600">
                        <v-card-title>
                            <span class="text-h5">Add new movie</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="newMovie.name" label="Name"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="newMovie.director" label="Director"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="newMovie.year" label="Year"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="newMovie.company" label="Company"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="newMovie.rating" label="Rating"></v-text-field>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="close()">Cancel</v-btn>
                            <v-btn color="blue darken-1" text @click="addElement()">Save</v-btn>
                        </v-card-actions>
                    </v-card>
                    <v-dialog v-model="dialogDelete" persistent width="auto">
                        <template v-slot:activator="{ props }">
                            <v-btn color="red darken-1" dark class="ma-2" v-bind="props" @click="dialogDelete = true">
                                Delete
                            </v-btn>
                        </template>
                        <v-card>
                            <v-card-title class="headline">Are you sure you want to delete the selected movie(s) from the table?</v-card-title>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue darken-1" text @click="dialogDelete = false">Cancel</v-btn>
                                <v-btn color="blue darken-1" text @click="deleteElements();dialogDelete = false">OK</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-btn color="blue darken-1" class="ma-2" v-on="selected.length === 1 ? {click: () => {editing = true; editMovie = Object.assign({}, selected[0])}} : {}" :disabled="selected.length !== 1">
                        Edit
                    </v-btn>
                    <v-card v-if="editing && selected.length===1" class="mx-auto" max-width="600">
                        <v-card-title>
                            <span class="text-h5">Edit selected movie</span>
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="editMovie.name" label="Name"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="editMovie.director" label="Director"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="editMovie.year" label="Year"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="editMovie.company" label="Company"></v-text-field>
                                    </v-col>
                                    <v-col cols="12" sm="6" md="4">
                                        <v-text-field v-model="editMovie.rating" label="Rating"></v-text-field>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn color="blue darken-1" text @click="editing = false">Cancel</v-btn>
                            <v-btn color="blue darken-1" text @click="editElement()">Save</v-btn>
                        </v-card-actions>
                    </v-card>
                    <v-text-field v-model="search" @change="fetchData()" v-if="editing === false" label="Search" append-icon="mdi-magnify" single-line hide-details></v-text-field>
                </v-row>
                <v-col cols="12">
                    <v-data-table
                        v-model="selected"
                        :headers="headers"
                        :items="products"
                        :page.sync="page"
                        @update:page="offset = $event;fetchData()"
                        :items-per-page.sync="limit"
                        @update:items-per-page="limit = $event;fetchData()"
                        :server-items-length="totalProducts"
                        show-select
                        class="elevation-1"
                        :loading="loading"
                        :sort-by.sync="sortBy"
                        @update:sort-by="sortBy = $event;fetchData()"
                        :sort-desc.sync="sortDesc"
                        @update:sort-desc="sortDesc = $event;fetchData()"
                        :search.sync="search"
                        @input:search="search = $event;fetchData()"
                    ></v-data-table>
                </v-col>
            </template>
        </v-app>
    </v-card>
</template>

<script>

import axios, {options} from "axios";

export default {
    name: 'App',
    components: {},
    data: () => ({
        products: [],
        selected: [],
        sortBy: 'id',
        sortDesc: false,
        loading: true,
        headers: [
            { text: 'Id', value: 'id' },
            { text: 'Name', value: 'name' },
            { text: 'Director', value: 'director' },
            { text: 'Year', value: 'year' },
            { text: 'Company', value: 'company' },
            { text: 'Rating', value: 'rating' }
        ],
        dialogDelete: false,
        adding: false,
        editing: false,
        editBody: '',
        limit: 5,
        page: 1,
        offset: 0,
        totalProducts: 0,
        newMovie: {
            name: '',
            director: '',
            year: '',
            company: '',
            rating: ''
        },
        editMovie: {
            id: '',
            name: '',
            director: '',
            year: '',
            company: '',
            rating: ''
        },
        search: ''
    }),
    watch: {
        options: {
            handler() {
                this.fetchData()
            },
            deep:true
        },
    },
    methods: {
        options,
        async fetchData() {
            this.loading = true;
            this.offset = (this.page-1) * this.limit;
            //console.log(this.offset);
            let search = '';
            if (this.search !== '') {
                search = '&search=' + this.search + '%'
            }
             await axios.get('http://localhost:8000/items/?offset=' + (this.offset)
                                                        + '&limit=' + this.limit
                                                        + '&sort=' + this.sortBy
                                                        + '&order=' + (this.sortDesc ? 'desc' : 'asc')
                                                        + search)
                .then(response => {
                    this.loading = false;
                    this.totalProducts = response.data.total;
                    this.products = response.data.items;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        // async fetchData() {
        //     this.loading = true;
        //     this.offset = (this.page-1) * this.limit;
        //     //console.log(this.offset);
        //     let search = '';
        //     if (this.search !== '') {
        //         search = '&search=%' + this.search + '%'
        //     }
        //     await fetch('http://localhost:8000/items/?offset=' + (this.offset)
        //                                                 + '&limit=' + this.limit
        //                                                 + '&sort=' + this.sortBy
        //                                                 + search)
        //         .then(response => response.json())
        //         .then(data => {
        //             this.loading = false;
        //             this.totalProducts = data.total;
        //             this.products = data.items;
        //         })
        //         .catch(error => {
        //             console.log(error);
        //         });
        // },
        close() {
            this.adding = false;
        },
        async addElement() {
            await axios.post('http://localhost:8000/items/', this.newMovie)
            this.newMovie = {
                name: '',
                director: '',
                year: '',
                company: '',
                rating: ''
            };
            this.fetchData();
            this.close();
        },
        async editElement() {
            console.log(this.selected[0])
            const response = await axios.put(`http://localhost:8000/items/${this.selected[0].id}`, {
                name: this.editMovie.name,
                director: this.editMovie.director,
                year: this.editMovie.year,
                company: this.editMovie.company,
                rating: this.editMovie.rating
            })
            console.log(response.data);
            this.selected = [];
            this.fetchData();
            this.editMovie = {
                id: '',
                name: '',
                director: '',
                year: '',
                company: '',
                rating: ''
            };
            this.editing = false;
        },
        async deleteElements() {
            const promises = this.selected.map(item => axios.delete(`http://localhost:8000/items/${item.name}/`));
            //console.log(promises);
            const r = await Promise.all(promises);
            console.log(r);
            this.fetchData();
            this.selected = [];
        },
    },
    mounted() {
        this.fetchData();
    }
};

</script>
