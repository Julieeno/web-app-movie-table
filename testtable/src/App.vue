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
                    <v-dialog
                            v-model="filters"
                            max-width="600px"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                                color="grey"
                                v-bind="attrs"
                                v-on="on"
                                >
                                Filters
                            </v-btn>
                        </template>
                        <v-card>
                            <v-toolbar
                                dark
                                >
                                <v-btn
                                    icon
                                    color="grey"
                                    @click="filters = false"
                                    >
                                    <v-icon>mdi-close</v-icon>
                                </v-btn>
                                <v-toolbar-title>Filters</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <v-toolbar-items>
            <v-btn
              dark
              text
              @click="yearFilter || ratingFilter ? getFilteredItems() : fetchData();filters = false"
            >
              Save
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <v-list
          three-line
          subheader
        >
          <v-list-item>
            <v-list-item-action>
              <v-checkbox v-model="yearFilter"></v-checkbox>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Year</v-list-item-title>
              <v-list-item-subtitle>Apply a filter on the year</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
            <v-card v-if="yearFilter">
                  <v-container>
                      <v-row>
                          <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="yearMin" label="Min"></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="yearMax" label="Max"></v-text-field>
                          </v-col>
                      </v-row>
                  </v-container>
              </v-card>
          <v-list-item>
            <v-list-item-action>
              <v-checkbox v-model="ratingFilter"></v-checkbox>
            </v-list-item-action>
              <v-list-item-content>
              <v-list-item-title>Rating</v-list-item-title>
              <v-list-item-subtitle>Apply a filter on ratings</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
            <v-card v-if="ratingFilter">
                  <v-container>
                      <v-row>
                          <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="ratingMin" label="Min"></v-text-field>
                          </v-col>
                          <v-col cols="12" sm="6" md="4">
                              <v-text-field v-model="ratingMax" label="Max"></v-text-field>
                          </v-col>
                      </v-row>
                  </v-container>
              </v-card>
        </v-list>
                        </v-card>
                    </v-dialog>
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
        filters: false,
        filter: '',
        yearFilter: false,
        yearMin: null,
        yearMax: null,
        ratingFilter: false,
        ratingMin: null,
        ratingMax: null,
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

             await axios.get('http://localhost:8000/items/', {
                 params: {
                     offset: this.offset,
                     limit: this.limit,
                     sort: this.sortBy,
                     order: this.sortDesc ? 'desc' : 'asc',
                     search: this.search ? '%' + this.search + '%' : null
                 }
             })
                .then(response => {
                    this.loading = false;
                    this.totalProducts = response.data.total;
                    this.products = response.data.items;
                })
                .catch(error => {
                    console.log(error);
                });
        },
        async getFilteredItems()    {
            console.log(this.yearMin,this.yearMax);

            await axios.get(`http://localhost:8000/items/filters`, {
                params: {
                    yearMin: this.yearMin ? parseInt(this.yearMin) : null,
                    yearMax: this.yearMax ? parseInt(this.yearMax) : null,
                    ratingMin: this.ratingMin ? parseFloat(this.ratingMin) : null,
                    ratingMax: this.ratingMax ? parseFloat(this.ratingMax) : null
                }
            })
              .then(response => {
                  this.loading = false;
                  this.totalProducts = response.data.total;
                  this.products = response.data.items;
              })
              .catch(error => {
                  console.log(error);
              });
        },
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
